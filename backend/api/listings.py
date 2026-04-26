from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import Listing, Property
from schemas import ListingResponse
from auth import verify_token
from worker import generate_listings_task

router = APIRouter(tags=["listings"])


@router.post(
    "/api/properties/{property_id}/listings/generate",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Générer les annonces (Agent Rédacteur)",
    description=(
        "Déclenche l'**Agent Rédacteur** qui génère 4 annonces adaptées à chaque plateforme "
        "(`seloger`, `leboncoin`, `pap`, `website`) via GPT-4o.\n\n"
        "Retourne immédiatement un `202 Accepted`. "
        "Interroge **GET /api/properties/{property_id}/listings** pour récupérer les annonces une fois générées."
    ),
)
def trigger_generate_listings(
    property_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    if not db.get(Property, property_id):
        raise HTTPException(status_code=404, detail="Bien introuvable")
    background_tasks.add_task(generate_listings_task, str(property_id))
    return {"message": "Génération des annonces en cours", "property_id": str(property_id)}


@router.get(
    "/api/properties/{property_id}/listings",
    response_model=list[ListingResponse],
    summary="Lister les annonces d'un bien",
)
def list_listings(
    property_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    if not db.get(Property, property_id):
        raise HTTPException(status_code=404, detail="Bien introuvable")
    q = select(Listing).where(Listing.property_id == property_id).order_by(Listing.created_at)
    return db.execute(q).scalars().all()


@router.get(
    "/api/listings/{listing_id}",
    response_model=ListingResponse,
    summary="Détail d'une annonce",
)
def get_listing(
    listing_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Annonce introuvable")
    return listing


@router.patch(
    "/api/listings/{listing_id}/approve",
    response_model=ListingResponse,
    summary="Approuver une annonce",
    description="Passe le statut de l'annonce de `draft` à `approved`.",
)
def approve_listing(
    listing_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Annonce introuvable")
    listing.status = "approved"
    db.commit()
    db.refresh(listing)
    return listing
