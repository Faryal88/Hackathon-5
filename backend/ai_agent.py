import openai
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import KnowledgeBase, Customer, Conversation, Message, Ticket
from schemas import ChannelEnum, StatusEnum, PriorityEnum
import os
from dotenv import load_dotenv
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Initialize OpenAI client for v1.x API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SearchKnowledgeBaseTool(BaseModel):
    """Tool for searching the knowledge base"""
    query: str


class CreateTicketTool(BaseModel):
    """Tool for creating a support ticket"""
    customer_id: int
    conversation_id: int
    issue: str
    priority: str


class GetCustomerHistoryTool(BaseModel):
    """Tool for retrieving customer interaction history"""
    customer_id: int


class EscalateToHumanTool(BaseModel):
    """Tool for escalating to human agent"""
    conversation_id: int
    reason: str


class SendResponseTool(BaseModel):
    """Tool for sending responses through appropriate channels"""
    conversation_id: int
    content: str
    channel: str


class AIAgent:
    def __init__(self, db: Session):
        self.db = db
        self.tools = {
            "search_knowledge_base": self.search_knowledge_base,
            "create_ticket": self.create_ticket,
            "get_customer_history": self.get_customer_history,
            "escalate_to_human": self.escalate_to_human,
            "send_response": self.send_response,
        }

    def search_knowledge_base(self, query: str) -> str:
        """Search the knowledge base for relevant information"""
        try:
            # Perform similarity search in the knowledge base
            knowledge_entries = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.question.ilike(f"%{query}%") |
                KnowledgeBase.answer.ilike(f"%{query}%") |
                KnowledgeBase.category.ilike(f"%{query}%")
            ).limit(5).all()

            if knowledge_entries:
                results = []
                for entry in knowledge_entries:
                    results.append(f"Q: {entry.question}\nA: {entry.answer}")
                return "\n\n".join(results)
            else:
                return "No relevant information found in the knowledge base."
        except Exception as e:
            return f"Error searching knowledge base: {str(e)}"

    def create_ticket(self, customer_id: int, conversation_id: int, issue: str, priority: str = "medium") -> str:
        """Create a support ticket"""
        try:
            ticket = Ticket(
                customer_id=customer_id,
                conversation_id=conversation_id,
                issue=issue,
                priority=priority
            )
            self.db.add(ticket)
            self.db.commit()
            self.db.refresh(ticket)
            return f"Ticket #{ticket.id} created successfully with {priority} priority."
        except Exception as e:
            return f"Error creating ticket: {str(e)}"

    def get_customer_history(self, customer_id: int) -> str:
        """Retrieve customer interaction history"""
        try:
            customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                return "Customer not found."

            conversations = self.db.query(Conversation).filter(
                Conversation.customer_id == customer_id
            ).order_by(Conversation.created_at.desc()).limit(5).all()

            if not conversations:
                return f"No previous interactions found for customer {customer.name}."

            history = f"Customer: {customer.name} ({customer.email})\nRecent Interactions:\n"
            for conv in conversations:
                messages = self.db.query(Message).filter(
                    Message.conversation_id == conv.id
                ).order_by(Message.timestamp.asc()).limit(3).all()

                history += f"- {conv.channel} conversation on {conv.created_at.strftime('%Y-%m-%d %H:%M')} (Status: {conv.status})\n"
                for msg in messages[:1]:  # Show first message as summary
                    preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    history += f"  > {msg.direction}: {preview}\n"

            return history
        except Exception as e:
            return f"Error retrieving customer history: {str(e)}"

    def escalate_to_human(self, conversation_id: int, reason: str) -> str:
        """Escalate conversation to human agent"""
        try:
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()

            if conversation:
                conversation.status = StatusEnum.escalated
                self.db.commit()

                # Create/update ticket with escalation status
                ticket = self.db.query(Ticket).filter(
                    Ticket.conversation_id == conversation_id
                ).first()

                if ticket:
                    ticket.status = StatusEnum.escalated
                    ticket.assigned_agent = "human_agent"
                    self.db.commit()

                return f"Conversation escalated to human agent. Reason: {reason}"
            else:
                return "Conversation not found for escalation."
        except Exception as e:
            return f"Error escalating to human: {str(e)}"

    def send_response(self, conversation_id: int, content: str, channel: str) -> str:
        """Send response through appropriate channel"""
        try:
            # Create outgoing message record
            message = Message(
                conversation_id=conversation_id,
                content=content,
                channel=channel,
                direction="outgoing"
            )
            self.db.add(message)
            self.db.commit()

            # Handle different channels appropriately
            if channel == "web_form":
                # For web_form channel, send email notification to user
                conversation = self.db.query(Conversation).filter(
                    Conversation.id == conversation_id
                ).first()

                if conversation:
                    customer = self.db.query(Customer).filter(
                        Customer.id == conversation.customer_id
                    ).first()

                    if customer and customer.email:
                        # In a real implementation, this would send an email
                        print(f"EMAIL TO {customer.email}: {content}")

            elif channel == "whatsapp":
                # For WhatsApp, get the phone number to send response back
                conversation = self.db.query(Conversation).filter(
                    Conversation.id == conversation_id
                ).first()

                if conversation:
                    customer = self.db.query(Customer).filter(
                        Customer.id == conversation.customer_id
                    ).first()

                    if customer and customer.phone:
                        # Actually send WhatsApp message via Twilio
                        success = self.send_whatsapp_message(customer.phone, content)
                        if success:
                            return f"WhatsApp response sent to {customer.phone} via Twilio."
                        else:
                            return f"Failed to send WhatsApp response to {customer.phone}."

            elif channel == "gmail":
                # For Gmail, send email response
                conversation = self.db.query(Conversation).filter(
                    Conversation.id == conversation_id
                ).first()

                if conversation:
                    customer = self.db.query(Customer).filter(
                        Customer.id == conversation.customer_id
                    ).first()

                    if customer and customer.email:
                        # Actually send email reply using Gmail API
                        success = self.send_gmail_reply(customer.email, content, conversation_id)
                        if success:
                            return f"Email response sent to {customer.email} via Gmail."
                        else:
                            return f"Failed to send email response to {customer.email}."

            return f"Response sent to conversation {conversation_id} via {channel}."
        except Exception as e:
            return f"Error sending response: {str(e)}"

    def send_gmail_reply(self, recipient_email: str, content: str, conversation_id: int) -> bool:
        """Send a reply email using SMTP"""
        try:
            # Get email configuration from environment
            smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
            username = os.getenv("EMAIL_USERNAME", "aimoshahs@gmail.com")
            password = os.getenv("EMAIL_PASSWORD", "jzjw ikvw nctw xkkc")
            from_name = os.getenv("EMAIL_FROM_NAME", "AI Employee")

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = f"{from_name} <{username}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Re: Support Request #{conversation_id}"

            # Add content to the message
            msg.attach(MIMEText(content, 'plain'))

            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable encryption
            server.login(username, password)

            text = msg.as_string()
            server.sendmail(username, recipient_email, text)
            server.quit()

            print(f"Email sent successfully to {recipient_email}")
            return True

        except Exception as e:
            print(f"Error sending Gmail reply: {str(e)}")
            return False

    def send_whatsapp_message(self, to_phone: str, content: str) -> bool:
        """Send a WhatsApp message using Twilio"""
        try:
            # Import Twilio here to avoid errors if the library isn't installed
            from twilio.rest import Client

            # Get Twilio configuration from environment
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            from_number = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

            # Validate that we have the required credentials
            if not account_sid or not auth_token:
                print("Twilio credentials not found in environment variables")
                return False

            # Initialize Twilio client
            client = Client(account_sid, auth_token)

            # Send WhatsApp message
            message = client.messages.create(
                body=content,
                from_=from_number,
                to=f"whatsapp:{to_phone}"
            )

            print(f"WhatsApp message sent successfully to {to_phone}. SID: {message.sid}")
            return True

        except ImportError:
            print("Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

    def should_escalate(self, message_content: str) -> tuple[bool, str]:
        """Check if message should be escalated to human agent"""
        content_lower = message_content.lower()

        # Check for escalation triggers
        # Removed 'pricing' and 'billing' from escalation keywords since these can be handled with knowledge base
        escalation_keywords = [
            'refund', 'cancel', 'contract',
            'legal', 'ceo', 'competitor', 'complaint', 'angry',
            'frustrated', 'threat', 'breach', 'security', 'hacker'
        ]

        for keyword in escalation_keywords:
            if keyword in content_lower:
                return True, f"Triggered by keyword: {keyword}"

        # Check for escalation patterns
        escalation_patterns = [
            r'dispute.*bill', r'cancel.*subscription',
            r'legal.*matter', r'ceo.*speak', r'competitor.*better'
        ]

        for pattern in escalation_patterns:
            if re.search(pattern, content_lower):
                return True, f"Triggered by pattern: {pattern}"

        return False, ""

    async def process_message(self, message_content: str, customer_id: int, conversation_id: int, channel: str) -> str:
        """Process a message with the AI agent"""
        try:
            # Get company information for context
            company_info = ""
            try:
                with open("company_info.txt", "r") as f:
                    company_info = f.read()
            except FileNotFoundError:
                company_info = "TechCorp is a leading provider of AI-powered analytics solutions for businesses of all sizes."

            # Different response strategies based on channel
            if channel == "whatsapp":
                # For WhatsApp, use more concise responses suitable for chat format
                ai_response = await self.generate_whatsapp_response(message_content, company_info)
            elif channel in ["web_form", "gmail"]:
                # For web form and email, use more formal responses suitable for email
                ai_response = await self.generate_email_response(message_content, company_info)
            else:
                # Default response for other channels
                ai_response = await self.generate_general_response(message_content, company_info)

            # Create outgoing message
            self.send_response(conversation_id, ai_response, channel)

            return ai_response

        except Exception as e:
            error_msg = f"I apologize, but I encountered an error processing your request: {str(e)}. I'll connect you with a human agent who can assist you further."
            self.escalate_to_human(conversation_id, f"AI processing error: {str(e)}")
            return error_msg

    async def generate_whatsapp_response(self, message_content: str, company_info: str) -> str:
        """Generate a response optimized for WhatsApp communication"""
        # First, try to find relevant information in the knowledge base
        relevant_kb = self.search_knowledge_base(message_content.lower())

        # Check if escalation is needed
        should_escalate, reason = self.should_escalate(message_content)

        # If we found relevant knowledge base information, use it
        if relevant_kb and "No relevant information found" not in relevant_kb:
            # More concise format for WhatsApp
            ai_response = f"Thanks for your inquiry! Based on our knowledge base:\n\n{relevant_kb}\n\nNeed more help?"
            return ai_response

        # If the message doesn't require escalation, provide tailored response
        if not should_escalate:
            lower_content = message_content.lower()

            # Check for common questions and provide WhatsApp-optimized answers
            if any(word in lower_content for word in ["price", "cost", "pricing", "plan", "plans", "subscription", "billing"]):
                ai_response = "Thanks for asking about pricing! 📊 We offer Basic ($29), Pro ($99), and Enterprise ($299) plans. Which would suit your needs best?"

            elif any(word in lower_content for word in ["reset", "password", "login", "account", "access"]):
                ai_response = "Need help with login? Just click 'Forgot Password' on the login page and follow the email instructions. Still having issues? 😤"

            elif any(word in lower_content for word in ["integrate", "integration", "api", "connect", "system"]):
                ai_response = "We've got APIs & connectors for Salesforce, GA & more! Check our docs for integration guides. Specific system? 🤔"

            elif any(word in lower_content for word in ["security", "privacy", "data", "protect"]):
                ai_response = "🔒 Security is our priority! SOC 2 compliant with end-to-end encryption. GDPR & CCPA compliant. Feel safe! 😊"

            elif any(word in lower_content for word in ["upgrade", "downgrade", "change", "modify"]):
                ai_response = "Easy to change plans! Upgrades are immediate, downgrades at next billing cycle. Want to switch now? 🔄"

            else:
                # General response for WhatsApp
                ai_response = f"Got your message! 📩 I'm addressing '{message_content[:50]}...' based on our training data. Need more help? 💬"
        else:
            # For WhatsApp, provide a concise escalation message
            ai_response = f"Need expert help! 🚀 Connecting you to a human agent about: {reason[:50]}..."

        return ai_response

    async def generate_email_response(self, message_content: str, company_info: str) -> str:
        """Generate a response optimized for email communication"""
        # First, try to find relevant information in the knowledge base
        relevant_kb = self.search_knowledge_base(message_content.lower())

        # Check if escalation is needed
        should_escalate, reason = self.should_escalate(message_content)

        # If we found relevant knowledge base information, use it
        if relevant_kb and "No relevant information found" not in relevant_kb:
            ai_response = f"Dear Customer,\n\nThank you for your inquiry. Based on our knowledge base:\n\n{relevant_kb}\n\nPlease let us know if you need any further assistance.\n\nBest regards,\nTechCorp Support Team"
            return ai_response

        # If the message doesn't require escalation, provide detailed email response
        if not should_escalate:
            lower_content = message_content.lower()

            # Check for common questions and provide detailed email answers
            if any(word in lower_content for word in ["price", "cost", "pricing", "plan", "plans", "subscription", "billing"]):
                ai_response = f"Dear Customer,\n\nThank you for your inquiry about our pricing plans. We offer three options:\n- Basic Plan: $29/month\n- Professional Plan: $99/month\n- Enterprise Plan: $299/month\nEach plan includes different features and data limits. Please visit our website for a detailed comparison.\n\nBest regards,\nTechCorp Support Team"

            elif any(word in lower_content for word in ["reset", "password", "login", "account", "access"]):
                ai_response = f"Dear Customer,\n\nThank you for contacting us regarding account access. To reset your password, please click the 'Forgot Password' link on the login page. Enter your email address and follow the instructions sent to your inbox. If you continue to experience difficulties, please provide more details about the specific issue you're encountering.\n\nBest regards,\nTechCorp Support Team"

            elif any(word in lower_content for word in ["integrate", "integration", "api", "connect", "system"]):
                ai_response = f"Dear Customer,\n\nThank you for your interest in our integration capabilities. Our platform offers REST APIs, webhooks, and pre-built connectors for popular platforms including Salesforce, Google Analytics, and Microsoft Dynamics. Detailed integration guides are available in our documentation portal.\n\nBest regards,\nTechCorp Support Team"

            elif any(word in lower_content for word in ["security", "privacy", "data", "protect"]):
                ai_response = f"Dear Customer,\n\nThank you for your question about our security measures. We maintain SOC 2 Type II compliance, implement end-to-end encryption, and conduct regular security audits. All data is encrypted, and we comply with GDPR and CCPA regulations. Our security measures include secure data storage, access controls, and regular penetration testing.\n\nBest regards,\nTechCorp Support Team"

            elif any(word in lower_content for word in ["upgrade", "downgrade", "change", "modify"]):
                ai_response = f"Dear Customer,\n\nRegarding plan changes: Yes, you can modify your plan at any time. Downgrades take effect at the next billing cycle, while upgrades are implemented immediately with prorated charges. Your data and settings will be preserved during the transition.\n\nBest regards,\nTechCorp Support Team"

            else:
                # General formal email response
                ai_response = f"Dear Customer,\n\nThank you for contacting TechCorp support. We have received your inquiry regarding '{message_content[:100]}...' and are addressing it based on our knowledge base. Our team will follow up with you within 2 business hours during normal business hours.\n\nIs there any additional detail you can provide to help us assist you better?\n\nBest regards,\nTechCorp Support Team"
        else:
            # For email, provide a formal escalation message
            ai_response = f"Dear Customer,\n\nWe understand this requires special attention. I've escalated your request to a human support agent who will contact you shortly.\n\nBest regards,\nTechCorp Support Team"

        return ai_response

    async def generate_general_response(self, message_content: str, company_info: str) -> str:
        """Generate a general response for other channels"""
        # Fallback to original logic for other channels
        # First, try to find relevant information in the knowledge base
        relevant_kb = self.search_knowledge_base(message_content.lower())

        # Check if escalation is needed
        should_escalate, reason = self.should_escalate(message_content)

        # If we found relevant knowledge base information, use it
        if relevant_kb and "No relevant information found" not in relevant_kb:
            ai_response = f"Thank you for your inquiry. Based on our knowledge base:\n\n{relevant_kb}\n\nIs there anything else I can help you with?"
            return ai_response

        # If the message doesn't require escalation, provide general response
        if not should_escalate:
            lower_content = message_content.lower()

            # Check for common questions and provide direct answers
            if any(word in lower_content for word in ["price", "cost", "pricing", "plan", "plans", "subscription", "billing"]):
                ai_response = "Thank you for your inquiry about pricing. According to our records, we offer Basic ($29/month), Professional ($99/month), and Enterprise ($299/month) plans with different features and data limits. For more specific information, please let me know what features you're interested in."

            elif any(word in lower_content for word in ["reset", "password", "login", "account", "access"]):
                ai_response = "Thank you for reaching out about account access. You can reset your password by clicking the 'Forgot Password' link on the login page. Enter your email address and follow the instructions sent to your inbox. If you continue to have issues, please provide more details about the specific problem you're experiencing."

            elif any(word in lower_content for word in ["integrate", "integration", "api", "connect", "system"]):
                ai_response = "Thank you for asking about integrations. Our platform offers REST APIs, webhooks, and pre-built connectors for popular platforms like Salesforce, Google Analytics, and Microsoft Dynamics. You can find detailed integration guides in our documentation portal. Would you like information about integrating with a specific system?"

            elif any(word in lower_content for word in ["security", "privacy", "data", "protect"]):
                ai_response = "Thank you for your question about security. We maintain SOC 2 Type II compliance, end-to-end encryption, and regular security audits. All data is encrypted and we comply with GDPR and CCPA regulations. Our security measures include secure data storage, access controls, and regular penetration testing."

            elif any(word in lower_content for word in ["upgrade", "downgrade", "change", "modify"]):
                ai_response = "Regarding plan changes: Yes, you can change your plan anytime. Downgrades take effect at the next billing cycle, while upgrades are immediate with prorated charges. Your data and settings will be preserved during the transition. Would you like to make a change to your current plan?"

            else:
                # General response
                ai_response = f"Thank you for contacting TechCorp support. I've reviewed your inquiry: '{message_content[:100]}...' and I'm addressing it based on our knowledge base. Our team will follow up with you within 2 hours during business hours. Is there any additional detail you can provide to help me assist you better?"
        else:
            # Escalate if needed
            ai_response = f"I understand this requires special attention. I'm connecting you with a human agent regarding: {reason}"

        return ai_response

    def extract_pricing_info(self, company_info):
        """Extract pricing information from company info"""
        lines = company_info.split('\n')
        pricing_lines = []

        for line in lines:
            if any(word in line.lower() for word in ["pricing", "plan", "cost", "price", "$"]):
                pricing_lines.append(line.strip())

        if pricing_lines:
            return "\n".join(pricing_lines[:5])  # Return first 5 pricing-related lines
        else:
            return "Our pricing includes Basic ($29/month), Professional ($99/month), and Enterprise ($299/month) plans with varying features and data limits."

    async def handle_escalation(self, conversation_id: int, reason: str, original_message: str) -> str:
        """Handle escalation to human agent"""
        try:
            # Escalate the conversation
            escalation_result = self.escalate_to_human(conversation_id, reason)

            # Prepare escalation message
            escalation_msg = (
                "I understand this requires special attention. "
                "I've escalated your request to a human support agent who will contact you shortly. "
                f"Reason for escalation: {reason}."
            )

            # Log the escalation
            print(f"ESCALATION: Conversation {conversation_id} escalated. Reason: {reason}")

            # Send escalation message
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()

            if conversation:
                self.send_response(conversation_id, escalation_msg, conversation.channel)

            return escalation_msg

        except Exception as e:
            return f"Error during escalation: {str(e)}"
