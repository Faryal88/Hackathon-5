from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
import asyncio
import hashlib
import hmac
import json
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
import time
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from starlette.responses import Response
from starlette.responses import Response

from database import engine, get_db
from models import Base, Customer as CustomerModel, Conversation as ConversationModel, Message as MessageModel, Ticket as TicketModel, KnowledgeBase as KnowledgeBaseModel
from schemas import (
    SupportRequest, SupportResponse, DashboardStats,
    Customer as CustomerSchema, Conversation as ConversationSchema, Message as MessageSchema, Ticket as TicketSchema, KnowledgeBase as KnowledgeBaseSchema
)
from enhanced_ai_agent import EnhancedAIAgent
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Import new modules
from kafka_client import FTEKafkaProducer, TOPICS
from admin_routes import admin_router

load_dotenv()

# Email configuration from environment variables
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "aimoshahs@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "jzjw ikvw nctw xkkc")
EMAIL_IMAP_SERVER = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
EMAIL_IMAP_PORT = int(os.getenv("EMAIL_IMAP_PORT", "993"))
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Abdullah AI Customer Support", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting Abdullah AI Customer Support API")

    # Initialize Kafka producer
    try:
        kafka_producer = FTEKafkaProducer()
        kafka_producer.start()
        # Store in app state
        app.state.kafka_producer = kafka_producer
        print("Kafka producer initialized successfully")
    except Exception as e:
        print(f"Warning: Failed to initialize Kafka producer: {e}")
        app.state.kafka_producer = None

    # Automatic email polling disabled - use manual triggers only
    # To process emails, manually call: curl -X POST http://localhost:8000/webhooks/gmail

    # To process emails manually, call: curl -X POST http://localhost:8080/webhooks/gmail

@app.get("/")
async def root():
    return {"message": "Welcome to TechCorp AI Customer Support API"}

@app.post("/api/support/submit", response_model=SupportResponse)
async def submit_support_request(request: SupportRequest, db: Session = Depends(get_db)):
    """Submit a support request via web form"""
    try:
        # Find or create customer
        customer = db.query(CustomerModel).filter(CustomerModel.email == request.email).first()
        if not customer:
            customer = CustomerModel(
                email=request.email,
                name=request.name,
                phone=None  # Phone not provided in web form
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Create conversation
        conversation = ConversationModel(
            customer_id=customer.id,
            channel="web_form",
            status="open"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        # Create initial message
        message = MessageModel(
            conversation_id=conversation.id,
            content=f"Subject: {request.subject}\nCategory: {request.category}\nMessage: {request.message}",
            channel="web_form",
            direction="incoming"
        )
        db.add(message)
        db.commit()

        # Create ticket
        ticket = TicketModel(
            customer_id=customer.id,
            conversation_id=conversation.id,
            issue=request.message,
            priority=request.priority.value
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        # Process with enhanced AI agent in background
        ai_agent = EnhancedAIAgent(db)
        response_content = await ai_agent.process_message(
            message.content,
            customer.id,
            conversation.id,
            "web_form"
        )

        return SupportResponse(
            success=True,
            message=response_content,
            ticket_id=ticket.id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing support request: {str(e)}")

@app.post("/webhooks/gmail")
async def gmail_webhook_manual(request: Request, db: Session = Depends(get_db)):
    """Manual trigger to check for new emails via IMAP"""
    try:
        # This endpoint can be called manually or via scheduled job
        # to check for new emails
        processed_count = await check_new_emails(db)

        return {"success": True, "message": f"Checked emails, processed {processed_count} new message(s)"}

    except Exception as e:
        print(f"Error processing email check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing email check: {str(e)}")

async def check_new_emails(db: Session):
    """Check for new emails using IMAP"""
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(EMAIL_IMAP_SERVER, EMAIL_IMAP_PORT)
        mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Select inbox
        mail.select('inbox')

        # Search for unseen emails
        status, messages = mail.search(None, 'UNSEEN')

        if status != 'OK':
            return 0

        email_ids = messages[0].split()
        processed_count = 0

        for email_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(email_id, '(RFC822)')

            if status != 'OK':
                continue

            # Parse the email
            msg = email.message_from_bytes(msg_data[0][1])

            # Extract email details
            sender = msg.get('From', '')
            subject = msg.get('Subject', '')

            # Extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8')

            # Find or create customer
            customer = db.query(CustomerModel).filter(CustomerModel.email == sender).first()
            if not customer:
                # Extract name from email if not already in system
                name_parts = sender.split('<')[0].strip().split()
                name = ' '.join(name_parts) if name_parts else sender.split('@')[0]

                customer = CustomerModel(
                    email=sender,
                    name=name,
                    phone=None
                )
                db.add(customer)
                db.commit()
                db.refresh(customer)

            # Create conversation
            conversation = ConversationModel(
                customer_id=customer.id,
                channel="gmail",
                status="open"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            # Create message
            message = MessageModel(
                conversation_id=conversation.id,
                content=f"Subject: {subject}\nFrom: {sender}\n\n{body}",
                channel="gmail",
                direction="incoming"
            )
            db.add(message)
            db.commit()

            # Create ticket
            ticket = TicketModel(
                customer_id=customer.id,
                conversation_id=conversation.id,
                issue=f"{subject[:50]}...: {body[:150]}..." if len(body) > 150 else f"{subject}: {body}",
                priority="medium"
            )
            db.add(ticket)
            db.commit()
            db.refresh(ticket)

            # Process with enhanced AI agent
            ai_agent = EnhancedAIAgent(db)
            response_content = await ai_agent.process_message(
                message.content,
                customer.id,
                conversation.id,
                "gmail"
            )

            # Save the AI response to the database first
            outgoing_message = MessageModel(
                conversation_id=conversation.id,
                content=response_content,
                channel="gmail",
                direction="outgoing"
            )
            db.add(outgoing_message)
            db.commit()

            # Then try to send response back to the sender via email (non-blocking)
            try:
                # Create and send email response
                email_msg = MIMEMultipart()
                email_msg['From'] = EMAIL_USERNAME
                email_msg['To'] = sender
                email_msg['Subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject

                # Add the AI response to the email body
                email_body = f"{response_content}\n\n---\nThis is an automated response from Abdullah AI Customer Support."
                email_msg.attach(MIMEText(email_body, 'plain'))

                # Connect to SMTP server and send email
                smtp_server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
                smtp_server.starttls()
                smtp_server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

                text = email_msg.as_string()
                smtp_server.sendmail(EMAIL_USERNAME, sender, text)
                smtp_server.quit()

                print(f"✅ Email response sent to {sender}: {response_content[:100]}...")

            except Exception as email_error:
                print(f"❌ Error sending email response: {str(email_error)}")
                print(f"⚠️  Response saved to database but not sent via email")

            processed_count += 1

        # Close the connection
        mail.close()
        mail.logout()

        return processed_count

    except Exception as e:
        print(f"Error checking emails: {str(e)}")
        return 0

# Function to periodically check for emails (runs in background)
def start_email_polling():
    """Start polling for new emails in the background"""
    def poll_emails():
        while True:
            try:
                # Create a new database session for this thread
                from database import SessionLocal
                db = SessionLocal()

                processed_count = asyncio.run(check_new_emails(db))
                print(f"Email polling completed: {processed_count} emails processed")

                db.close()

                # Wait for 5 minutes before next check
                time.sleep(300)
            except Exception as e:
                print(f"Error in email polling: {str(e)}")
                time.sleep(300)  # Wait before retrying even if there's an error

    # Start the polling thread
    # DISABLED: Automatic polling removed - use manual triggers only
    # email_thread = Thread(target=poll_emails, daemon=True)
    # email_thread.start()
    # print("Started email polling in background...")
    print("Email polling is disabled - use manual webhook triggers only")

@app.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Parse form-encoded data from Twilio
        form_data = await request.form()

        from_number = form_data.get("From", "")
        to_number = form_data.get("To", "")
        body = form_data.get("Body", "")
        message_sid = form_data.get("MessageSid", "")
        account_sid = form_data.get("AccountSid", "")

        print(f"Received WhatsApp message from {from_number}: {body}")

        # Get Twilio credentials from environment
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        # Normalize phone number format
        phone = from_number.replace("whatsapp:", "")

        # Find or create customer
        customer = db.query(CustomerModel).filter(CustomerModel.phone == phone).first()

        # If no customer found by phone, check if one exists with a temporary email for this phone
        # (handles cases where customer was created from WhatsApp without phone initially stored)
        if not customer:
            temp_email = f"{phone.replace('+', '').replace('-', '').replace(' ', '')}@whatsapp.temp"
            customer = db.query(CustomerModel).filter(CustomerModel.email == temp_email).first()

        # If still no customer found, create a new one
        if not customer:
            temp_email = f"{phone.replace('+', '').replace('-', '').replace(' ', '')}@whatsapp.temp"
            customer = CustomerModel(
                email=temp_email,  # Use generated temporary email to satisfy NOT NULL constraint
                name=phone,  # Use phone as name temporarily
                phone=phone
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Create conversation
        conversation = ConversationModel(
            customer_id=customer.id,
            channel="whatsapp",
            status="open"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        # Create message
        message = MessageModel(
            conversation_id=conversation.id,
            content=body,
            channel="whatsapp",
            direction="incoming"
        )
        db.add(message)
        db.commit()

        # Create ticket
        ticket = TicketModel(
            customer_id=customer.id,
            conversation_id=conversation.id,
            issue=body[:200] + "..." if len(body) > 200 else body,
            priority="medium"
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        # Process with enhanced AI agent in background
        ai_agent = EnhancedAIAgent(db)
        response_content = await ai_agent.process_message(
            message.content,
            customer.id,
            conversation.id,
            "whatsapp"
        )

        print(f"AI generated response: {response_content}")

        # Send response back to WhatsApp using Twilio
        twilio_send_success = False
        if twilio_account_sid and twilio_auth_token and twilio_whatsapp_number:
            try:
                client = Client(twilio_account_sid, twilio_auth_token)

                # Send the response back to WhatsApp
                message_response = client.messages.create(
                    body=response_content,
                    from_=twilio_whatsapp_number,  # Your WhatsApp number from env
                    to=from_number
                )

                print(f"✅ SENT TO WHATSAPP {from_number}: {response_content}")
                print(f"Twilio Message SID: {message_response.sid}")
                twilio_send_success = True
            except Exception as twilio_error:
                print(f"❌ Error sending response to WhatsApp: {str(twilio_error)}")
                # Continue anyway to return TwiML response to Twilio
        else:
            print("⚠️ Twilio credentials not configured, skipping response sending")

        # Create TwiML response for Twilio - this is what Twilio expects as acknowledgment
        # This is critical: Twilio needs to receive a valid TwiML response
        resp = MessagingResponse()

        # Optionally, you can add a message to the TwiML response
        # This is what Twilio will send back as an immediate response
        # For WhatsApp, we typically don't need to add a message here since we're sending via API
        # But adding an empty one ensures proper TwiML format

        # Return the TwiML response to Twilio with proper XML content type
        xml_content = str(resp)
        print(f"Returning TwiML response to Twilio: {xml_content}")

        return Response(
            content=xml_content,
            media_type="text/xml",  # Changed from application/xml to text/xml
            headers={"Content-Type": "text/xml"}
        )

    except Exception as e:
        print(f"❌ Error processing WhatsApp webhook: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full stack trace for debugging

        # Return minimal valid TwiML response to prevent Twilio from retrying
        resp = MessagingResponse()
        return Response(
            content=str(resp),
            media_type="text/xml",
            headers={"Content-Type": "text/xml"},
            status_code=200
        )


@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    try:
        # Total tickets
        total_tickets = db.query(TicketModel).count()

        # Active conversations (open or processing)
        active_conversations = db.query(ConversationModel).filter(
            ConversationModel.status.in_(["open", "processing"])
        ).count()

        # Escalations
        escalations = db.query(TicketModel).filter(
            TicketModel.status == "escalated"
        ).count()

        # Average response time (calculate from message timestamps)
        # For simplicity, calculating average time between incoming and outgoing messages
        avg_response_time = 0.0

        # In a real implementation, this would calculate actual response times
        # For now, returning a placeholder value
        avg_response_time = 120.5  # in seconds

        return DashboardStats(
            total_tickets=total_tickets,
            active_conversations=active_conversations,
            escalations=escalations,
            avg_response_time=avg_response_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard stats: {str(e)}")

@app.get("/api/conversations", response_model=List[ConversationSchema])
async def get_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of conversations"""
    try:
        conversations = db.query(ConversationModel).offset(skip).limit(limit).all()
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")

@app.get("/api/messages/{conversation_id}", response_model=List[MessageSchema])
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get messages for a specific conversation"""
    try:
        messages = db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")


@app.get("/api/tickets/user", response_model=dict)
async def get_user_tickets(email: str, db: Session = Depends(get_db)):
    """Get tickets for a specific user by email"""
    try:
        # Find customer by email
        customer = db.query(CustomerModel).filter(CustomerModel.email == email).first()

        if not customer:
            raise HTTPException(status_code=404, detail="No customer found with this email")

        # Find all tickets for this customer
        tickets = db.query(TicketModel).filter(TicketModel.customer_id == customer.id).all()

        # Get conversation details for each ticket
        tickets_with_details = []
        for ticket in tickets:
            conversation = db.query(ConversationModel).filter(ConversationModel.id == ticket.conversation_id).first()
            messages = db.query(MessageModel).filter(MessageModel.conversation_id == ticket.conversation_id).all()

            ticket_detail = {
                "id": ticket.id,
                "issue": ticket.issue,
                "status": ticket.status,
                "priority": ticket.priority,
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at,
                "conversation_channel": conversation.channel if conversation else None,
                "conversation_status": conversation.status if conversation else None,
                "messages": [{
                    "id": msg.id,
                    "content": msg.content,
                    "direction": msg.direction,
                    "timestamp": msg.timestamp
                } for msg in messages]
            }
            tickets_with_details.append(ticket_detail)

        return {
            "customer": {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name
            },
            "tickets": tickets_with_details,
            "count": len(tickets_with_details)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user tickets: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Abdullah AI Customer Support API")

    # Close Kafka producer if it exists
    if hasattr(app.state, 'kafka_producer') and app.state.kafka_producer:
        app.state.kafka_producer.close()
        print("Kafka producer closed")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Include admin routes
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
