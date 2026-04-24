from celery import Celery
from config import get_settings

settings = get_settings()

celery_app = Celery(
    "autopilot",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Paris",
    enable_utc=True,
)


@celery_app.task(name="analyze_document")
def analyze_document_task(document_id: str):
    """Placeholder — sera remplacé par l'Agent Analyste (semaine 3)."""
    from database import SessionLocal
    from models import Document

    db = SessionLocal()
    try:
        doc = db.get(Document, document_id)
        if doc:
            doc.status = "processing"
            db.commit()
            # TODO: Agent Analyste
            doc.status = "done"
            db.commit()
    finally:
        db.close()


@celery_app.task(name="generate_listings")
def generate_listings_task(property_id: str):
    """Placeholder — sera remplacé par l'Agent Rédacteur (semaine 4)."""
    pass


@celery_app.task(name="send_followup")
def send_followup_task(lead_id: str):
    """Placeholder — sera remplacé par les relances automatiques (semaine 18)."""
    pass
