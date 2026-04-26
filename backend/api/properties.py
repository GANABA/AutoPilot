from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Property
from schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from auth import verify_token

router = APIRouter(prefix="/api/properties", tags=["properties"])


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED, summary="Créer un bien")
def create_property(body: PropertyCreate, db: Session = Depends(get_db), _=Depends(verify_token)):
    prop = Property(**body.model_dump(exclude={"metadata_"}), metadata_=body.metadata_)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.get("", response_model=list[PropertyResponse], summary="Lister les biens")
def list_properties(
    status: str | None = None,
    city: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    q = select(Property)
    if status:
        q = q.where(Property.status == status)
    if city:
        q = q.where(Property.city.ilike(f"%{city}%"))
    q = q.order_by(Property.created_at.desc())
    return db.execute(q).scalars().all()


@router.get("/{property_id}", response_model=PropertyResponse, summary="Récupérer un bien")
def get_property(property_id: UUID, db: Session = Depends(get_db), _=Depends(verify_token)):
    prop = db.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Bien introuvable")
    return prop


@router.put("/{property_id}", response_model=PropertyResponse, summary="Modifier un bien")
def update_property(property_id: UUID, body: PropertyUpdate, db: Session = Depends(get_db), _=Depends(verify_token)):
    prop = db.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Bien introuvable")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un bien")
def delete_property(property_id: UUID, db: Session = Depends(get_db), _=Depends(verify_token)):
    prop = db.get(Property, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Bien introuvable")
    db.delete(prop)
    db.commit()
