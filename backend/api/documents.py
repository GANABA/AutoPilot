from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from database import get_db
from models import Document
from schemas import DocumentResponse
from services.storage import upload_file
from auth import verify_token
from worker import analyze_document_task

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    property_id: UUID | None = Form(None),
    db: Session = Depends(get_db),
    _=Depends(verify_token),
):
    content = await file.read()
    file_key = f"documents/{uuid4()}/{file.filename}"
    file_url = await upload_file(content, file_key, file.content_type or "application/octet-stream")

    doc = Document(
        property_id=property_id,
        filename=file.filename,
        file_url=file_url,
        status="pending",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Déclenche l'analyse en arrière-plan
    analyze_document_task.delay(str(doc.id))

    return doc


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: UUID, db: Session = Depends(get_db), _=Depends(verify_token)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document introuvable")
    return doc
