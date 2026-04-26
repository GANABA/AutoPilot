from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import select
from config import get_settings

settings = get_settings()
_client = OpenAI(api_key=settings.openai_api_key)


def embed_text(text: str) -> list[float]:
    response = _client.embeddings.create(
        input=text[:8000],
        model=settings.embedding_model,
    )
    return response.data[0].embedding


def property_to_text(prop) -> str:
    parts = [
        prop.title or "",
        f"{prop.type or ''} {prop.nb_rooms or ''}p {prop.surface or ''}m²",
        f"{prop.city or ''} {prop.zipcode or ''}",
        f"{prop.price or ''}€",
        f"DPE {prop.energy_class}" if prop.energy_class else "",
        "balcon" if prop.has_balcony else "",
        "parking" if prop.has_parking else "",
        "ascenseur" if prop.has_elevator else "",
        prop.description or "",
    ]
    return " | ".join(p for p in parts if p.strip())


def search_similar_properties(db: Session, query_embedding: list[float], limit: int = 3):
    from models import Property
    return db.execute(
        select(Property)
        .where(Property.embedding.isnot(None))
        .where(Property.status == "active")
        .order_by(Property.embedding.cosine_distance(query_embedding))
        .limit(limit)
    ).scalars().all()


def embed_property_bg(property_id: str):
    """Background task — génère et stocke l'embedding d'un bien."""
    from database import SessionLocal
    from models import Property

    db = SessionLocal()
    try:
        prop = db.get(Property, property_id)
        if prop:
            prop.embedding = embed_text(property_to_text(prop))
            db.commit()
    finally:
        db.close()
