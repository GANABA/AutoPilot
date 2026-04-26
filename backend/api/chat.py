import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from openai import OpenAI
from database import get_db
from models import Conversation, Message, Lead
from schemas import ChatRequest, ChatResponse, ConversationDetail
from auth import verify_widget_or_token
from services.embeddings import embed_text, search_similar_properties
from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/chat", tags=["chat"])

_SYSTEM_PROMPT = """\
Tu es l'assistant virtuel de {agency_name}, une agence immobilière française.
Ton rôle : aider les prospects à trouver un bien, répondre à leurs questions et proposer des visites.
Ton style : {brand_voice}.

Biens disponibles dans notre catalogue :
{properties_context}

Règles :
- Réponds uniquement en français.
- Propose uniquement des biens présents dans le catalogue ci-dessus.
- Si le prospect semble intéressé par un bien, propose de planifier une visite.
- Collecte naturellement le nom et l'email du prospect si possible.
- Si aucun bien ne correspond, dis-le honnêtement et propose de rappeler.
- Ne réponds pas aux questions hors immobilier.
"""


def _format_properties(props) -> str:
    if not props:
        return "Aucun bien trouvé dans le catalogue."
    lines = []
    for p in props:
        line = f"- [{p.id}] {p.title or 'Sans titre'}"
        if p.price:
            line += f" — {int(p.price):,} €".replace(",", " ")
        if p.surface:
            line += f" — {p.surface}m²"
        if p.nb_rooms:
            line += f" — {p.nb_rooms}p"
        if p.city:
            line += f" — {p.city}"
        if p.energy_class:
            line += f" — DPE {p.energy_class}"
        lines.append(line)
    return "\n".join(lines)


def _extract_lead_info(text: str) -> dict | None:
    """Tente d'extraire nom/email/téléphone du message utilisateur."""
    client = OpenAI(api_key=settings.openai_api_key)
    try:
        resp = client.chat.completions.create(
            model=settings.llm_simple_model,
            response_format={"type": "json_object"},
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extrait les informations de contact si présentes dans le texte. "
                        "Retourne un JSON : {\"name\": string|null, \"email\": string|null, \"phone\": string|null}. "
                        "Retourne null pour les champs absents."
                    ),
                },
                {"role": "user", "content": text},
            ],
        )
        data = json.loads(resp.choices[0].message.content)
        if any(v for v in data.values() if v):
            return data
    except Exception:
        pass
    return None


router_chat = router


@router.post("", response_model=ChatResponse, summary="Envoyer un message au chatbot")
def chat(body: ChatRequest, db: Session = Depends(get_db)):
    # Récupère ou crée la conversation
    conv = None
    if body.conversation_id:
        conv = db.get(Conversation, body.conversation_id)
    if not conv:
        conv = Conversation(channel="chatbot")
        db.add(conv)
        db.flush()

    # Historique des messages (max 10 derniers)
    history = db.execute(
        select(Message)
        .where(Message.conversation_id == conv.id)
        .order_by(Message.created_at.desc())
        .limit(10)
    ).scalars().all()
    history = list(reversed(history))

    # RAG — recherche les biens pertinents
    query_embedding = embed_text(body.message)
    similar_props = search_similar_properties(db, query_embedding, limit=4)

    # Construit le système
    system = _SYSTEM_PROMPT.format(
        agency_name=settings.agency_name,
        brand_voice=settings.agency_brand_voice,
        properties_context=_format_properties(similar_props),
    )

    # Appel GPT
    client = OpenAI(api_key=settings.openai_api_key)
    messages_payload = [{"role": "system", "content": system}]
    for m in history:
        messages_payload.append({"role": m.role, "content": m.content})
    messages_payload.append({"role": "user", "content": body.message})

    response = client.chat.completions.create(
        model=settings.llm_complex_model,
        temperature=0.5,
        messages=messages_payload,
    )
    reply = response.choices[0].message.content

    # Sauvegarde les messages
    db.add(Message(conversation_id=conv.id, role="user", content=body.message))
    db.add(Message(conversation_id=conv.id, role="assistant", content=reply))

    # Tentative de capture du lead si info de contact détectée
    lead_info = _extract_lead_info(body.message)
    if lead_info and not conv.lead_id:
        lead = Lead(
            name=lead_info.get("name"),
            email=lead_info.get("email"),
            phone=lead_info.get("phone"),
            source="chatbot",
            gdpr_consent=True,
        )
        db.add(lead)
        db.flush()
        conv.lead_id = lead.id

    db.commit()

    return ChatResponse(
        reply=reply,
        conversation_id=conv.id,
        suggested_property_ids=[str(p.id) for p in similar_props],
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetail,
    summary="Historique d'une conversation",
)
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db), _=Depends(verify_widget_or_token)):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    messages = db.execute(
        select(Message)
        .where(Message.conversation_id == conv.id)
        .order_by(Message.created_at)
    ).scalars().all()
    return ConversationDetail(
        id=conv.id,
        channel=conv.channel,
        status=conv.status,
        lead_id=conv.lead_id,
        created_at=conv.created_at,
        messages=[{"role": m.role, "content": m.content, "created_at": m.created_at} for m in messages],
    )
