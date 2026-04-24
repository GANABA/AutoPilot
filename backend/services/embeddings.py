from openai import OpenAI
from config import get_settings

settings = get_settings()
_client = OpenAI(api_key=settings.openai_api_key)


def embed_text(text: str) -> list[float]:
    response = _client.embeddings.create(
        input=text,
        model=settings.embedding_model,
    )
    return response.data[0].embedding


def property_to_text(prop) -> str:
    parts = [
        prop.title or "",
        f"{prop.type or ''} {prop.nb_rooms or ''}p {prop.surface or ''}m²",
        f"{prop.city or ''} {prop.zipcode or ''}",
        f"{prop.price or ''}€",
        prop.description or "",
    ]
    return " | ".join(p for p in parts if p.strip())
