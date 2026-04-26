import ssl
import time
from celery import Celery
from config import get_settings

settings = get_settings()

celery_app = Celery(
    "autopilot",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

_ssl_opts = {"ssl_cert_reqs": ssl.CERT_NONE} if settings.redis_url.startswith("rediss://") else {}

celery_app.conf.update(
    broker_use_ssl=_ssl_opts or None,
    redis_backend_use_ssl=_ssl_opts or None,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=True,
)


@celery_app.task(name="analyze_document")
def analyze_document_task(document_id: str):
    from database import SessionLocal
    from models import Document, Property
    from services.storage import download_file
    from services.analyzer import analyze

    db = SessionLocal()
    doc = None
    start = time.time()
    try:
        doc = db.get(Document, document_id)
        if not doc:
            return

        doc.status = "processing"
        db.commit()

        pdf_bytes = download_file(doc.file_url)
        result = analyze(pdf_bytes)

        doc.doc_type = result["doc_type"]
        doc.extracted_data = {"confidence": result["confidence"], **result["data"]}
        doc.status = "done"

        # Auto-enrichit le bien associé si c'est un DPE
        if result["doc_type"] == "dpe" and doc.property_id and result["data"].get("energy_class"):
            prop = db.get(Property, doc.property_id)
            if prop:
                prop.energy_class = result["data"]["energy_class"]

        db.commit()

    except Exception as e:
        if doc:
            doc.status = "error"
            doc.extracted_data = {"error": str(e)}
            db.commit()
        raise
    finally:
        db.close()


@celery_app.task(name="generate_listings")
def generate_listings_task(property_id: str):
    """Placeholder — Agent Rédacteur (semaine 4)."""
    pass


@celery_app.task(name="send_followup")
def send_followup_task(lead_id: str):
    """Placeholder — relances automatiques (semaine 6)."""
    pass
