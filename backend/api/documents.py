from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from database import get_db
from models import Document, Property
from schemas import DocumentResponse
from services.storage import upload_file
from auth import verify_token
from worker import analyze_document_task

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Uploader un PDF",
    description=(
        "Upload un fichier PDF et déclenche l'**Agent Analyste** en arrière-plan.\n\n"
        "Le document passe par les statuts : `pending` → `processing` → `done` (ou `error`).\n\n"
        "Interroge **GET /{document_id}** pour récupérer le résultat une fois `status=done`. "
        "Le champ `extracted_data` contiendra les données extraites (classe DPE, prix du mandat, etc.)."
    ),
)
async def upload_document(
    file: UploadFile = File(..., description="Fichier PDF (DPE, mandat de vente, PV de copropriété...)"),
    property_id: UUID | None = Form(None, description="UUID du bien à associer (optionnel — laisser vide si aucun)"),
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    if property_id and not db.get(Property, property_id):
        raise HTTPException(status_code=404, detail=f"Bien {property_id} introuvable")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide")

    file_key = f"documents/{uuid4()}/{file.filename}"
    try:
        file_url = await upload_file(content, file_key, file.content_type or "application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur upload R2 : {e}")

    doc = Document(
        property_id=property_id,
        filename=file.filename,
        file_url=file_url,
        status="pending",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    analyze_document_task.delay(str(doc.id))

    return doc


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Résultat de l'analyse",
    description="Retourne le document et le champ `extracted_data` une fois `status=done`.",
)
def get_document(document_id: UUID, db: Session = Depends(get_db), _=Depends(verify_token)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document introuvable")
    return doc
