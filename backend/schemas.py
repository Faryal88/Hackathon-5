from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ChannelEnum(str, Enum):
    web_form = "web_form"
    gmail = "gmail"
    whatsapp = "whatsapp"


class DirectionEnum(str, Enum):
    incoming = "incoming"
    outgoing = "outgoing"


class StatusEnum(str, Enum):
    open = "open"
    processing = "processing"
    resolved = "resolved"
    escalated = "escalated"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


# Customer Schemas
class CustomerBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Message Schemas
class MessageBase(BaseModel):
    conversation_id: int
    content: str
    channel: ChannelEnum
    direction: DirectionEnum


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    customer_id: int
    channel: ChannelEnum
    status: StatusEnum = StatusEnum.open


class ConversationCreate(ConversationBase):
    pass


class Conversation(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Ticket Schemas
class TicketBase(BaseModel):
    customer_id: int
    conversation_id: int
    issue: str
    status: StatusEnum = StatusEnum.open
    priority: PriorityEnum = PriorityEnum.medium
    assigned_agent: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Knowledge Base Schemas
class KnowledgeBaseBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    keywords: Optional[str] = None


class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass


class KnowledgeBase(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Request Schemas
class SupportRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    category: str
    message: str
    priority: PriorityEnum = PriorityEnum.medium


# Response Schemas
class SupportResponse(BaseModel):
    success: bool
    message: str
    ticket_id: Optional[int] = None


# Dashboard Stats Schema
class DashboardStats(BaseModel):
    total_tickets: int
    active_conversations: int
    escalations: int
    avg_response_time: float
