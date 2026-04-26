from uuid import UUID, uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
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
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Fichier PDF (DPE, mandat de vente, PV de copropriété...)"),
    property_id: str | None = Form(None, description="UUID du bien à associer (optionnel — laisser vide si aucun)"),
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    pid: UUID | None = None
    if property_id:
        try:
            pid = UUID(property_id)
        except ValueError:
            raise HTTPException(status_code=422, detail="property_id n'est pas un UUID valide")
        if not db.get(Property, pid):
            raise HTTPException(status_code=404, detail=f"Bien {pid} introuvable")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide")

    file_key = f"documents/{uuid4()}/{file.filename}"
    try:
        file_url = await upload_file(content, file_key, file.content_type or "application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erreur upload R2 : {e}")

    doc = Document(
        property_id=pid,
        filename=file.filename,
        file_url=file_url,
        status="pending",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    background_tasks.add_task(analyze_document_task, str(doc.id))

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
