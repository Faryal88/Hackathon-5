from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    conversations = relationship("Conversation", back_populates="customer")
    tickets = relationship("Ticket", back_populates="customer")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel = Column(String, nullable=False)  # 'web_form', 'gmail', 'whatsapp'
    status = Column(String, default='open')  # 'open', 'processing', 'resolved', 'escalated'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    ticket = relationship("Ticket", back_populates="conversation", uselist=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text, nullable=False)
    channel = Column(String, nullable=False)  # 'web_form', 'gmail', 'whatsapp'
    direction = Column(String, nullable=False)  # 'incoming', 'outgoing'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    issue = Column(Text, nullable=False)
    status = Column(String, default='open')  # 'open', 'in_progress', 'resolved', 'escalated'
    priority = Column(String, default='medium')  # 'low', 'medium', 'high', 'urgent'
    assigned_agent = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="tickets")
    conversation = relationship("Conversation", back_populates="ticket")


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String)
    keywords = Column(String)  # Storing as comma-separated values
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
