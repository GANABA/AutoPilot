from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Lead
from schemas import LeadCreate, LeadResponse
from auth import verify_token

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(body: LeadCreate, db: Session = Depends(get_db), _=Depends(verify_token)):
    lead = Lead(**body.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=list[LeadResponse])
def list_leads(status: str | None = None, db: Session = Depends(get_db), _=Depends(verify_token)):
    q = select(Lead)
    if status:
        q = q.where(Lead.status == status)
    q = q.order_by(Lead.created_at.desc())
    return db.execute(q).scalars().all()


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: UUID, db: Session = Depends(get_db), _=Depends(verify_token)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    return lead


@router.patch("/{lead_id}/status", response_model=LeadResponse)
def update_lead_status(lead_id: UUID, new_status: str, db: Session = Depends(get_db), _=Depends(verify_token)):
    lead = db.get(Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead introuvable")
    lead.status = new_status
    db.commit()
    db.refresh(lead)
    return lead
