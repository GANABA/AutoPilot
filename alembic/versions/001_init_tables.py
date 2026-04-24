"""init tables

Revision ID: 001
Revises:
Create Date: 2026-04-20
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON, UUID
from pgvector.sqlalchemy import Vector

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "properties",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("reference", sa.String(50)),
        sa.Column("type", sa.String(50)),
        sa.Column("title", sa.String(255)),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Float),
        sa.Column("surface", sa.Float),
        sa.Column("nb_rooms", sa.Integer),
        sa.Column("nb_bedrooms", sa.Integer),
        sa.Column("city", sa.String(100)),
        sa.Column("zipcode", sa.String(10)),
        sa.Column("address", sa.String(255)),
        sa.Column("floor", sa.Integer),
        sa.Column("has_balcony", sa.Boolean, server_default="false"),
        sa.Column("has_parking", sa.Boolean, server_default="false"),
        sa.Column("has_elevator", sa.Boolean, server_default="false"),
        sa.Column("energy_class", sa.String(5)),
        sa.Column("charges_monthly", sa.Float),
        sa.Column("photos", JSON, server_default="[]"),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("agent_name", sa.String(100)),
        sa.Column("agent_email", sa.String(100)),
        sa.Column("embedding", Vector(1536)),
        sa.Column("metadata", JSON, server_default="{}"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
    )
    op.create_index("ix_properties_status", "properties", ["status"])
    op.create_index("ix_properties_city", "properties", ["city"])

    op.create_table(
        "leads",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100)),
        sa.Column("email", sa.String(100)),
        sa.Column("phone", sa.String(20)),
        sa.Column("criteria", JSON),
        sa.Column("score", sa.Integer, server_default="0"),
        sa.Column("status", sa.String(30), server_default="new"),
        sa.Column("source", sa.String(30)),
        sa.Column("gdpr_consent", sa.Boolean, server_default="false"),
        sa.Column("gdpr_consent_at", sa.DateTime),
        sa.Column("last_contact_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "conversations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id")),
        sa.Column("status", sa.String(20), server_default="open"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", UUID(as_uuid=True), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("metadata", JSON, server_default="{}"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "documents",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("property_id", UUID(as_uuid=True), sa.ForeignKey("properties.id")),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("doc_type", sa.String(30)),
        sa.Column("extracted_data", JSON),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "listings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("property_id", UUID(as_uuid=True), sa.ForeignKey("properties.id"), nullable=False),
        sa.Column("platform", sa.String(30), nullable=False),
        sa.Column("title", sa.String(255)),
        sa.Column("content", sa.Text),
        sa.Column("status", sa.String(20), server_default="draft"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "visits",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("property_id", UUID(as_uuid=True), sa.ForeignKey("properties.id"), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=False),
        sa.Column("scheduled_at", sa.DateTime, nullable=False),
        sa.Column("status", sa.String(20), server_default="scheduled"),
        sa.Column("feedback_prospect", sa.Text),
        sa.Column("calendar_event_id", sa.String(100)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "tasks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("agent", sa.String(30), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("input_data", JSON, nullable=False),
        sa.Column("output_data", JSON),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("error_message", sa.Text),
        sa.Column("duration_ms", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("visits")
    op.drop_table("listings")
    op.drop_table("documents")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("leads")
    op.drop_table("properties")
