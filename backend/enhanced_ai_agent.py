import openai
import asyncio
from typing import Dict, Any, List, Optional
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
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import PyPDF2
from pathlib import Path

# Import notification service
from notification_service import notification_service

load_dotenv()

# Initialize OpenAI client for Gemini API
api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = openai.OpenAI(
    api_key=api_key,
    base_url=base_url
)

class EnhancedAIAgent:
    def __init__(self, db: Session):
        self.db = db
        self.tools = {
            "search_knowledge_base": self.search_knowledge_base,
            "create_ticket": self.create_ticket,
            "get_customer_history": self.get_customer_history,
            "escalate_to_human": self.escalate_to_human,
            "send_response": self.send_response,
        }
        # Initialize TF-IDF vectorizer for better semantic search
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.knowledge_embeddings = None
        self.knowledge_entries = []
        self.pdf_knowledge = []  # Store knowledge extracted from PDFs

        # Load and embed knowledge base for semantic search
        self._prepare_knowledge_base()
        # Load PDF knowledge if available
        self._load_pdf_knowledge()

    def _load_pdf_knowledge(self):
        """Load knowledge from PDF files in the knowledge directory"""
        try:
            # Look for PDF files in the project directory
            pdf_files = list(Path(".").glob("*.pdf")) + list(Path(".").glob("knowledge/*.pdf"))

            for pdf_file in pdf_files:
                print(f"Loading knowledge from PDF: {pdf_file}")
                pdf_content = self._extract_text_from_pdf(pdf_file)

                if pdf_content:
                    # Split PDF content into chunks for better processing
                    chunks = self._chunk_text(pdf_content, chunk_size=1000)

                    for i, chunk in enumerate(chunks):
                        self.pdf_knowledge.append({
                            "id": f"pdf_{pdf_file.name}_chunk_{i}",
                            "content": chunk,
                            "source": str(pdf_file.name),
                            "page": i + 1
                        })

            print(f"Loaded {len(self.pdf_knowledge)} knowledge chunks from PDFs")
        except Exception as e:
            print(f"Error loading PDF knowledge: {str(e)}")

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text content from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            return ""

    def _chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks of specified size"""
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
        return chunks

    def _prepare_knowledge_base(self):
        """Prepare knowledge base for semantic search"""
        try:
            # Retrieve all knowledge base entries
            knowledge_entries = self.db.query(KnowledgeBase).all()

            if knowledge_entries:
                self.knowledge_entries = knowledge_entries
                # Combine questions and answers for embedding
                texts = [f"{entry.question} {entry.answer}" for entry in knowledge_entries]

                # Create TF-IDF matrix
                self.knowledge_embeddings = self.vectorizer.fit_transform(texts)

        except Exception as e:
            print(f"Error preparing knowledge base: {str(e)}")

    def enhanced_search_knowledge_base(self, query: str) -> List[Dict]:
        """Enhanced semantic search in the knowledge base"""
        try:
            results = []

            # Search in database knowledge base
            if self.knowledge_embeddings is not None and self.knowledge_embeddings.shape[0] > 0:
                query_vector = self.vectorizer.transform([query])
                similarities = cosine_similarity(query_vector, self.knowledge_embeddings).flatten()

                top_indices = similarities.argsort()[-3:][::-1]  # Top 3 from DB

                for idx in top_indices:
                    if similarities[idx] > 0.1:  # Only include if similarity is above threshold
                        entry = self.knowledge_entries[idx]
                        results.append({
                            "question": entry.question,
                            "answer": entry.answer,
                            "category": entry.category,
                            "similarity": similarities[idx],
                            "source": "database"
                        })

            # Search in PDF knowledge with improved matching
            if self.pdf_knowledge:
                for pdf_chunk in self.pdf_knowledge:
                    # Enhanced search with multiple matching strategies
                    content_lower = pdf_chunk["content"].lower()
                    query_lower = query.lower()

                    # Exact phrase matching
                    phrase_match = query_lower in content_lower

                    # Word overlap matching
                    query_words = set(query_lower.split())
                    content_words = set(content_lower.split())
                    overlap = len(query_words.intersection(content_words))
                    word_similarity = overlap / max(len(query_words), 1)

                    # Calculate overall relevance score
                    if phrase_match:
                        similarity = min(1.0, 0.5 + word_similarity)  # Boost phrase matches
                    else:
                        similarity = word_similarity

                    if similarity > 0.1:  # Threshold for relevance
                        results.append({
                            "question": f"From {pdf_chunk['source']} (Page {pdf_chunk['page']})",
                            "answer": pdf_chunk["content"][:800] + "..." if len(pdf_chunk["content"]) > 800 else pdf_chunk["content"],  # Extended content
                            "category": "pdf_document",
                            "similarity": similarity,
                            "source": "pdf"
                        })

            # Sort by similarity score
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:5]  # Return top 5 results

        except Exception as e:
            print(f"Error in enhanced search: {str(e)}")
            # Fallback to basic search
            return self._basic_search(query)

    def _basic_search(self, query: str) -> List[Dict]:
        """Fallback basic search in the knowledge base"""
        try:
            knowledge_entries = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.question.ilike(f"%{query}%") |
                KnowledgeBase.answer.ilike(f"%{query}%") |
                KnowledgeBase.category.ilike(f"%{query}%")
            ).limit(3).all()

            results = []
            for entry in knowledge_entries:
                results.append({
                    "question": entry.question,
                    "answer": entry.answer,
                    "category": entry.category,
                    "similarity": 1.0,  # Placeholder for basic search
                    "source": "database"
                })

            # Also search in PDF knowledge with improved matching
            query_lower = query.lower()
            for pdf_chunk in self.pdf_knowledge:
                content_lower = pdf_chunk["content"].lower()

                # Multiple matching strategies for better recall
                exact_match = query_lower in content_lower
                word_present = any(word in content_lower for word in query_lower.split())

                if exact_match or word_present:
                    # Calculate a more nuanced similarity score
                    query_words = set(query_lower.split())
                    content_words = set(content_lower.split())
                    overlap = len(query_words.intersection(content_words))
                    similarity = overlap / max(len(query_words), 1) if query_words else 0

                    # Boost score for exact matches
                    if exact_match:
                        similarity = min(1.0, similarity + 0.3)

                    results.append({
                        "question": f"From {pdf_chunk['source']} (Page {pdf_chunk['page']})",
                        "answer": pdf_chunk["content"][:800] + "..." if len(pdf_chunk["content"]) > 800 else pdf_chunk["content"],  # Extended content
                        "category": "pdf_document",
                        "similarity": min(1.0, similarity + 0.5),  # Boost PDF results slightly
                        "source": "pdf"
                    })

            return results
        except Exception as e:
            print(f"Error in basic search: {str(e)}")
            return []

    def search_knowledge_base(self, query: str) -> str:
        """Search the knowledge base for relevant information"""
        results = self.enhanced_search_knowledge_base(query)

        if results:
            # Sort results by similarity score to prioritize most relevant
            sorted_results = sorted(results, key=lambda x: x["similarity"], reverse=True)

            formatted_results = []
            for result in sorted_results:
                if result["source"] == "pdf":
                    formatted_results.append(f"[PDF DOCUMENT] {result['question']}\nCONTENT: {result['answer']}")
                else:
                    formatted_results.append(f"[DATABASE] Q: {result['question']}\nA: {result['answer']}")
            return "\n\n".join(formatted_results)
        else:
            return "No relevant information found in the knowledge base or PDF documents."

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
                        # Send email using the configured SMTP credentials
                        print(f"Sending email to {customer.email}...")
                        self.send_gmail_reply(customer.email, content, conversation_id)

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
        escalation_keywords = [
            'refund', 'cancel', 'contract', 'legal', 'ceo', 'competitor',
            'complaint', 'angry', 'frustrated', 'threat', 'breach',
            'security', 'hacker', 'privacy', 'data leak', 'compliance',
            'ceo', 'executive', 'board', 'lawsuit', 'litigation'
        ]

        for keyword in escalation_keywords:
            if keyword in content_lower:
                return True, f"Triggered by keyword: {keyword}"

        # Check for escalation patterns
        escalation_patterns = [
            r'dispute.*bill', r'cancel.*subscription', r'legal.*matter',
            r'ceo.*speak', r'competitor.*better', r'breach.*security',
            r'hack.*account', r'data.*compromised', r'violation.*law',
            r'non.*compliance', r'audit.*requirement'
        ]

        for pattern in escalation_patterns:
            if re.search(pattern, content_lower):
                return True, f"Triggered by pattern: {pattern}"

        return False, ""

    async def process_message(self, message_content: str, customer_id: int, conversation_id: int, channel: str) -> str:
        """Process a message with the enhanced AI agent"""
        try:
            # Get company information for context
            company_info = ""
            try:
                # Try to read from current directory first, then from parent directory
                import os
                current_dir_file = "company_info.txt"
                parent_dir_file = "../company_info.txt"

                if os.path.exists(current_dir_file):
                    with open(current_dir_file, "r") as f:
                        company_info = f.read()
                elif os.path.exists(parent_dir_file):
                    with open(parent_dir_file, "r") as f:
                        company_info = f.read()
                else:
                    # Fallback to default info
                    company_info = "Abdullah AI is a leading provider of AI-powered analytics solutions for businesses of all sizes."
            except Exception:
                company_info = "Abdullah AI is a leading provider of AI-powered analytics solutions for businesses of all sizes."

            # Get customer history for context
            customer_context = self.get_customer_history(customer_id)

            # Get relevant knowledge base information (including PDF knowledge)
            relevant_kb = self.search_knowledge_base(message_content.lower())

            # Check if escalation is needed
            should_escalate, reason = self.should_escalate(message_content)

            if should_escalate:
                # Handle escalation
                return await self.handle_escalation(conversation_id, reason, message_content)

            # Generate response using OpenAI with context from PDFs and knowledge base
            ai_response = await self.generate_intelligent_response(
                message_content,
                company_info,
                customer_context,
                relevant_kb,
                channel
            )

            # Create outgoing message
            self.send_response(conversation_id, ai_response, channel)

            return ai_response

        except Exception as e:
            error_msg = f"I apologize, but I encountered an error processing your request: {str(e)}. I'll connect you with a human agent who can assist you further."
            self.escalate_to_human(conversation_id, f"AI processing error: {str(e)}")
            return error_msg

    async def generate_intelligent_response(self, message_content: str, company_info: str,
                                         customer_context: str, relevant_kb: str, channel: str) -> str:
        """Generate intelligent response using OpenAI with full context from PDFs and KB"""
        try:
            # Prepare context for the AI model with emphasis on PDF knowledge
            context_prompt = f"""
            You are an AI customer support agent for Abdullah AI, a leading SaaS company providing AI-powered analytics solutions.

            COMPANY INFORMATION:
            {company_info}

            CUSTOMER CONTEXT:
            {customer_context}

            RELEVANT KNOWLEDGE FROM PDF DOCUMENTS AND KNOWLEDGE BASE:
            {relevant_kb}

            MESSAGE FROM CUSTOMER:
            {message_content}

            INSTRUCTIONS:
            1. PROVIDE ACCURATE RESPONSES BASED ON THE PDF DOCUMENTS AND KNOWLEDGE BASE PROVIDED ABOVE
            2. If specific company policies, procedures, or detailed information exists in the PDFs, prioritize that information
            3. Use a tone appropriate for the channel: concise for WhatsApp, formal for email/web forms
            4. If the question is about pricing, plans, or features, refer to the company information and PDF documents
            5. If the customer seems frustrated or angry, acknowledge their concern and offer specific help
            6. If you don't have sufficient information in the provided knowledge, politely say so and offer to connect with a human agent
            7. Always maintain professionalism and empathy
            8. Format your response appropriately for the channel
            9. When citing information from PDFs, mention that the information comes from official company documents
            """

            # Call OpenAI API to generate response (mapped to Gemini)
            import os
            model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")  # Use Gemini model

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a highly knowledgeable customer support agent for Abdullah AI. Your responses must be accurate, helpful, and based on the provided company documentation (especially PDF documents) and knowledge base. Prioritize information from official documents over general knowledge. Be professional, empathetic, and provide specific answers based on the company's policies and procedures."},
                    {"role": "user", "content": context_prompt}
                ],
                max_tokens=800,  # Increased for more detailed responses from PDF knowledge
                temperature=0.5  # Lower temperature for more consistent, fact-based responses
            )

            ai_response = response.choices[0].message.content.strip()

            # Format response based on channel
            if channel == "whatsapp":
                # Make response more concise for WhatsApp while preserving important details
                if len(ai_response) > 500:
                    # Truncate if too long for WhatsApp but keep key information
                    lines = ai_response.split('\n')
                    shortened_lines = []
                    char_count = 0
                    for line in lines:
                        if char_count + len(line) <= 500:
                            shortened_lines.append(line)
                            char_count += len(line) + 1
                        else:
                            break
                    ai_response = '\n'.join(shortened_lines) + "\n\n(For complete details, please contact via email)"

            elif channel in ["web_form", "gmail"]:
                # Add professional closing for email
                ai_response += "\n\nBest regards,\nAbdullah AI Support Team\n(Powered by company documentation and knowledge base)"

            return ai_response

        except Exception as e:
            print(f"Error generating intelligent response: {str(e)}")
            # Fallback to rule-based response
            return await self.generate_fallback_response(message_content, channel)

    async def generate_fallback_response(self, message_content: str, channel: str) -> str:
        """Generate fallback response when OpenAI fails"""
        # This maintains the original functionality as backup
        if channel == "whatsapp":
            ai_response = f"Thanks for your message! I'm reviewing '{message_content[:50]}...' and will get back to you soon. Need more help? 💬"
        elif channel in ["web_form", "gmail"]:
            ai_response = f"Dear Customer,\n\nThank you for contacting Abdullah support. We have received your inquiry regarding '{message_content[:100]}...' and are addressing it based on our knowledge base. Our team will follow up with you within 2 business hours during normal business hours.\n\nIs there any additional detail you can provide to help us assist you better?\n\nBest regards,\nAbdullah Support Team"
        else:
            ai_response = f"Thank you for contacting Abdullah support. I've reviewed your inquiry: '{message_content[:100]}...' and I'm addressing it based on our knowledge base. Our team will follow up with you within 2 hours during business hours."

        return ai_response

    async def handle_escalation(self, conversation_id: int, reason: str, original_message: str) -> str:
        """Handle escalation to human agent with notifications"""
        try:
            # Get conversation and customer details for notification
            conversation = self.db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()

            customer = None
            ticket = None
            if conversation:
                customer = self.db.query(Customer).filter(
                    Customer.id == conversation.customer_id
                ).first()

                ticket = self.db.query(Ticket).filter(
                    Ticket.conversation_id == conversation_id
                ).first()

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

            # Send escalation notification to human agents
            if ticket and customer:
                try:
                    await notification_service.send_escalation_notification(
                        ticket_id=ticket.id,
                        customer_name=customer.name,
                        issue=ticket.issue,
                        priority=ticket.priority
                    )
                    print(f"Escalation notification sent for ticket #{ticket.id}")
                except Exception as notify_error:
                    print(f"Failed to send escalation notification: {notify_error}")

            # Send escalation message to customer
            if conversation:
                self.send_response(conversation_id, escalation_msg, conversation.channel)

            return escalation_msg

        except Exception as e:
            return f"Error during escalation: {str(e)}"

    async def update_knowledge_base(self, question: str, answer: str, category: str = ""):
        """Add new knowledge to the knowledge base"""
        try:
            # Check if this question already exists
            existing = self.db.query(KnowledgeBase).filter(
                KnowledgeBase.question.ilike(f"%{question}%")
            ).first()

            if not existing:
                # Create new knowledge base entry
                kb_entry = KnowledgeBase(
                    question=question,
                    answer=answer,
                    category=category
                )
                self.db.add(kb_entry)
                self.db.commit()

                # Rebuild knowledge base embeddings
                self._prepare_knowledge_base()

                return f"New knowledge added to the knowledge base: {question}"
            else:
                return f"Question already exists in knowledge base: {existing.question}"

        except Exception as e:
            return f"Error updating knowledge base: {str(e)}"

    async def load_new_pdf(self, pdf_path: str):
        """Load a new PDF file into the knowledge base"""
        try:
            pdf_content = self._extract_text_from_pdf(Path(pdf_path))

            if pdf_content:
                # Split PDF content into chunks for better processing
                chunks = self._chunk_text(pdf_content, chunk_size=1000)

                for i, chunk in enumerate(chunks):
                    self.pdf_knowledge.append({
                        "id": f"pdf_{Path(pdf_path).name}_chunk_{i}",
                        "content": chunk,
                        "source": str(Path(pdf_path).name),
                        "page": i + 1
                    })

                return f"Successfully loaded {len(chunks)} knowledge chunks from {pdf_path}"
            else:
                return f"Failed to extract content from {pdf_path}"

        except Exception as e:
            return f"Error loading PDF {pdf_path}: {str(e)}"

    async def learn_from_interaction(self, customer_query: str, ai_response: str, customer_satisfaction: int = 0):
        """Learn from successful interactions to improve future responses"""
        # This method could be extended to track which responses work well
        # and potentially add them to the knowledge base if they prove effective
        if customer_satisfaction >= 4:  # High satisfaction (scale 1-5)
            # This is where you could implement reinforcement learning
            # For now, just log the successful interaction
            print(f"Successfully learned from interaction: Query='{customer_query[:50]}...', Satisfaction={customer_satisfaction}")
