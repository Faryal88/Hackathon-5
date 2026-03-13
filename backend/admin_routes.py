from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from models import Ticket, Conversation, Customer, Message
from database import get_db
from schemas import Ticket as TicketSchema, Conversation as ConversationSchema, Message as MessageSchema
from datetime import datetime

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/login")
async def admin_login():
    """Admin login endpoint"""
    return {"message": "Admin login page"}

@admin_router.get("/dashboard")
async def admin_dashboard(db: Session = Depends(get_db)):
    """Admin dashboard with all tickets and escalations"""
    # Get all escalated tickets
    escalated_tickets = db.query(Ticket).filter(
        Ticket.status == "escalated"
    ).order_by(Ticket.created_at.desc()).all()

    # Get all tickets
    all_tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).limit(50).all()

    # Get stats
    total_tickets = db.query(Ticket).count()
    open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()
    escalated_count = len(escalated_tickets)

    return {
        "stats": {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "escalated_tickets": escalated_count,
            "recent_activity": len(all_tickets)
        },
        "escalated_tickets": [ticket.__dict__ for ticket in escalated_tickets],
        "recent_tickets": [ticket.__dict__ for ticket in all_tickets]
    }

@admin_router.get("/tickets/escalated", response_model=List[TicketSchema])
async def get_escalated_tickets(db: Session = Depends(get_db)):
    """Get all escalated tickets for human agents"""
    escalated_tickets = db.query(Ticket).filter(
        Ticket.status == "escalated"
    ).order_by(Ticket.created_at.desc()).all()

    return escalated_tickets

@admin_router.get("/tickets/assigned", response_model=List[TicketSchema])
async def get_assigned_tickets(agent_name: str, db: Session = Depends(get_db)):
    """Get tickets assigned to a specific agent"""
    assigned_tickets = db.query(Ticket).filter(
        Ticket.assigned_agent == agent_name
    ).order_by(Ticket.created_at.desc()).all()

    return assigned_tickets

@admin_router.put("/tickets/{ticket_id}/assign")
async def assign_ticket(ticket_id: int, agent_name: str, db: Session = Depends(get_db)):
    """Assign a ticket to a human agent"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.assigned_agent = agent_name
    ticket.status = "in_progress"
    ticket.updated_at = datetime.utcnow()

    db.commit()

    # Send assignment notification
    from notification_service import notification_service
    conversation = db.query(Conversation).filter(Conversation.id == ticket.conversation_id).first()
    customer = db.query(Customer).filter(Customer.id == ticket.customer_id).first() if conversation else None

    if customer:
        await notification_service.send_agent_assignment_notification(
            ticket_id=ticket.id,
            agent_name=agent_name,
            customer_name=customer.name,
            issue=ticket.issue
        )

    return {"message": f"Ticket {ticket_id} assigned to {agent_name}", "ticket": ticket.__dict__}

@admin_router.put("/tickets/{ticket_id}/update-status")
async def update_ticket_status(ticket_id: int, status: str, db: Session = Depends(get_db)):
    """Update ticket status"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    valid_statuses = ["open", "in_progress", "resolved", "closed", "escalated"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Valid statuses: {valid_statuses}")

    ticket.status = status
    ticket.updated_at = datetime.utcnow()
    db.commit()

    return {"message": f"Ticket {ticket_id} status updated to {status}", "ticket": ticket.__dict__}

@admin_router.get("/conversations/{conversation_id}/messages", response_model=List[MessageSchema])
async def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    """Get all messages in a conversation"""
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).all()

    return messages
