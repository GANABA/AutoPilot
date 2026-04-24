from uuid import uuid4
from datetime import datetime
from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer,
    String, Text, func
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from database import Base


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    reference: Mapped[str | None] = mapped_column(String(50))
    type: Mapped[str | None] = mapped_column(String(50))          # "appartement", "maison", "terrain"
    title: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float | None] = mapped_column(Float)
    surface: Mapped[float | None] = mapped_column(Float)
    nb_rooms: Mapped[int | None] = mapped_column(Integer)
    nb_bedrooms: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str | None] = mapped_column(String(100))
    zipcode: Mapped[str | None] = mapped_column(String(10))
    address: Mapped[str | None] = mapped_column(String(255))
    floor: Mapped[int | None] = mapped_column(Integer)
    has_balcony: Mapped[bool] = mapped_column(Boolean, default=False)
    has_parking: Mapped[bool] = mapped_column(Boolean, default=False)
    has_elevator: Mapped[bool] = mapped_column(Boolean, default=False)
    energy_class: Mapped[str | None] = mapped_column(String(5))
    charges_monthly: Mapped[float | None] = mapped_column(Float)
    photos: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="active")  # "active", "under_offer", "sold"
    agent_name: Mapped[str | None] = mapped_column(String(100))
    agent_email: Mapped[str | None] = mapped_column(String(100))
    embedding: Mapped[list | None] = mapped_column(Vector(1536))
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now())

    documents: Mapped[list["Document"]] = relationship("Document", back_populates="property")
    listings: Mapped[list["Listing"]] = relationship("Listing", back_populates="property")
    visits: Mapped[list["Visit"]] = relationship("Visit", back_populates="property")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(20))
    criteria: Mapped[dict | None] = mapped_column(JSON)
    score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="new")  # "new", "qualified", "visit_scheduled", "won", "lost"
    source: Mapped[str | None] = mapped_column(String(30))          # "chatbot", "email", "phone"
    gdpr_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    gdpr_consent_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_contact_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now())

    conversations: Mapped[list["Conversation"]] = relationship("Conversation", back_populates="lead")
    visits: Mapped[list["Visit"]] = relationship("Visit", back_populates="lead")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    channel: Mapped[str] = mapped_column(String(20))               # "chatbot", "email", "phone"
    lead_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"))
    status: Mapped[str] = mapped_column(String(20), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    lead: Mapped["Lead | None"] = relationship("Lead", back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))                  # "user", "assistant"
    content: Mapped[str] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("properties.id"))
    filename: Mapped[str] = mapped_column(String(255))
    file_url: Mapped[str] = mapped_column(String(500))
    doc_type: Mapped[str | None] = mapped_column(String(30))       # "dpe", "copro", "mandat", "other"
    extracted_data: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # "pending", "processing", "done", "error"
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    property: Mapped["Property | None"] = relationship("Property", back_populates="documents")


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("properties.id"))
    platform: Mapped[str] = mapped_column(String(30))              # "seloger", "leboncoin", "website"
    title: Mapped[str | None] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="draft")  # "draft", "approved"
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    property: Mapped["Property"] = relationship("Property", back_populates="listings")


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("properties.id"))
    lead_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")  # "scheduled", "done", "cancelled", "no_show"
    feedback_prospect: Mapped[str | None] = mapped_column(Text)
    calendar_event_id: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    property: Mapped["Property"] = relationship("Property", back_populates="visits")
    lead: Mapped["Lead"] = relationship("Lead", back_populates="visits")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    agent: Mapped[str] = mapped_column(String(30))                 # "support", "analyst", "writer", "voice", "orchestrator"
    action: Mapped[str] = mapped_column(String(100))
    input_data: Mapped[dict] = mapped_column(JSON)
    output_data: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # "pending", "running", "done", "error"
    error_message: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
