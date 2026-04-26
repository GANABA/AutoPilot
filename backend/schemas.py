from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {"email": "admin@immoplus.fr", "password": "MotDePasseSecurise123!"}
        }
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Property ──────────────────────────────────────────────────────────────────

class PropertyCreate(BaseModel):
    reference: str | None = None
    type: str | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    surface: float | None = None
    nb_rooms: int | None = None
    nb_bedrooms: int | None = None
    city: str | None = None
    zipcode: str | None = None
    address: str | None = None
    floor: int | None = None
    has_balcony: bool = False
    has_parking: bool = False
    has_elevator: bool = False
    energy_class: str | None = None
    charges_monthly: float | None = None
    photos: list[str] = []
    agent_name: str | None = None
    agent_email: str | None = None
    metadata_: dict = {}

    model_config = {
        "json_schema_extra": {
            "example": {
                "reference": "APT-001",
                "type": "appartement",
                "title": "Beau T3 avec balcon — Lyon 6e",
                "description": "Appartement lumineux de 68m² au 3e étage avec balcon plein sud.",
                "price": 285000,
                "surface": 68,
                "nb_rooms": 3,
                "nb_bedrooms": 2,
                "city": "Lyon",
                "zipcode": "69006",
                "address": "12 rue de Sèze",
                "floor": 3,
                "has_balcony": True,
                "has_parking": False,
                "has_elevator": True,
                "energy_class": "C",
                "charges_monthly": 180,
                "agent_name": "Sophie Martin",
                "agent_email": "s.martin@immoplus.fr",
            }
        }
    }

class PropertyUpdate(PropertyCreate):
    status: str | None = None

class PropertyResponse(PropertyCreate):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


# ── Lead ──────────────────────────────────────────────────────────────────────

class LeadCreate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    criteria: dict | None = None
    source: str | None = None
    gdpr_consent: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@email.fr",
                "phone": "0612345678",
                "criteria": {"budget_max": 300000, "surface_min": 60, "city": "Lyon"},
                "source": "chatbot",
                "gdpr_consent": True,
            }
        }
    }

class LeadResponse(LeadCreate):
    id: UUID
    score: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Document ──────────────────────────────────────────────────────────────────

class DocumentResponse(BaseModel):
    id: UUID
    property_id: UUID | None
    filename: str
    file_url: str
    doc_type: str | None
    extracted_data: dict | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Listing ───────────────────────────────────────────────────────────────────

class ListingResponse(BaseModel):
    id: UUID
    property_id: UUID
    platform: str
    title: str | None
    content: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
