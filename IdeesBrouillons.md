## Description du projet — AutoPilot Immo

### Vue d'ensemble

AutoPilot Immo est une une solution/système d'automatisation multi-agents intelligente pour les agences immobilières. Le système est composé de 5 agents IA spécialisés (Support, Analyste, Rédacteur, Vocal, Orchestrateur) qui collaborent pour automatiser les tâches répétitives d'une agence : répondre aux prospects, rédiger des annonces, analyser des documents, répondre au téléphone et coordonner le tout.

### Architecture

Le projet suit une architecture microservices avec un API Gateway central.

**Stack technique proposé:**
- Backend : Python 3.11+, FastAPI, Celery + Redis (tâches async), SQLAlchemy
- IA : LangChain, LangGraph (orchestration multi-agents), OpenAI API (GPT-4o-mini pour les tâches courantes, GPT-4o pour les tâches complexes)
- Base de données : PostgreSQL (données structurées : biens, clients, tâches, conversations), pgvector (base vectorielle pour le RAG, stockage des embeddings des annonces et documents)
- Cache/Queue : Redis (cache, mémoire court terme des agents, broker Celery)
- Voix : OpenAI Whisper (STT), ElevenLabs ou Coqui TTS (text-to-speech), Twilio (téléphonie)
- Intégrations : n8n (workflows d'intégration email/calendar), Google Calendar API, SendGrid (emails)
- Frontend : React + Tailwind CSS (dashboard agence), widget chatbot en JavaScript vanilla (à intégrer sur le site du client)
- Déploiement : Docker + Docker Compose, GitHub Actions (CI/CD)
- Tests : pytest, httpx (tests API)


### Modèles de données de base(PostgreSQL)

```python
# database/models.py

class Tenant(Base):
    """Une agence immobilière = un tenant"""
    __tablename__ = "tenants"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)          # "Agence ImmoPlus"
    slug = Column(String, unique=True)              # "immoplus-lyon"
    website_url = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    settings = Column(JSON, default={})             # Config spécifique (ton, templates)
    created_at = Column(DateTime, server_default=func.now())

class Property(Base):
    """Un bien immobilier"""
    __tablename__ = "properties"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    reference = Column(String)                      # "IMMO-2026-042"
    type = Column(String)                           # "appartement", "maison", "terrain"
    title = Column(String)
    description = Column(Text)
    price = Column(Float)
    surface = Column(Float)
    nb_rooms = Column(Integer)
    nb_bedrooms = Column(Integer)
    city = Column(String)
    zipcode = Column(String)
    address = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    has_balcony = Column(Boolean, default=False)
    has_parking = Column(Boolean, default=False)
    has_elevator = Column(Boolean, default=False)
    energy_class = Column(String, nullable=True)    # "A" à "G"
    charges_monthly = Column(Float, nullable=True)
    photos = Column(JSON, default=[])               # Liste d'URLs
    status = Column(String, default="active")       # "active", "under_offer", "sold"
    agent_name = Column(String, nullable=True)
    agent_email = Column(String, nullable=True)
    metadata = Column(JSON, default={})             # Données supplémentaires flexibles
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Conversation(Base):
    """Une conversation avec un prospect"""
    __tablename__ = "conversations"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"))
    channel = Column(String)                        # "web_chat", "email", "phone", "api"
    prospect_name = Column(String, nullable=True)
    prospect_email = Column(String, nullable=True)
    prospect_phone = Column(String, nullable=True)
    search_criteria = Column(JSON, nullable=True)   # Critères extraits par l'agent
    status = Column(String, default="open")         # "open", "qualified", "visit_booked", "closed"
    messages = relationship("Message", back_populates="conversation")
    created_at = Column(DateTime, server_default=func.now())

class Message(Base):
    """Un message dans une conversation"""
    __tablename__ = "messages"
    id = Column(UUID, primary_key=True, default=uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"))
    role = Column(String)                           # "user", "assistant", "system"
    content = Column(Text)
    metadata = Column(JSON, default={})             # Propriétés suggérées, confiance, etc.
    created_at = Column(DateTime, server_default=func.now())
    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    """Un document uploadé (DPE, copro, mandat)"""
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"))
    property_id = Column(UUID, ForeignKey("properties.id"), nullable=True)
    filename = Column(String)
    file_url = Column(String)
    doc_type = Column(String, nullable=True)        # "dpe", "copro", "mandat", "other"
    extracted_data = Column(JSON, nullable=True)    # Données extraites par l'analyste
    status = Column(String, default="pending")      # "pending", "processing", "done", "error"
    created_at = Column(DateTime, server_default=func.now())

class Listing(Base):
    """Une annonce générée"""
    __tablename__ = "listings"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"))
    property_id = Column(UUID, ForeignKey("properties.id"))
    platform = Column(String)                       # "leboncoin", "seloger", "website"
    title = Column(String)
    content = Column(Text)
    status = Column(String, default="draft")        # "draft", "approved", "published"
    created_at = Column(DateTime, server_default=func.now())

class Task(Base):
    """Une tâche exécutée par un agent ou un workflow"""
    __tablename__ = "tasks"
    id = Column(UUID, primary_key=True, default=uuid4)
    tenant_id = Column(UUID, ForeignKey("tenants.id"))
    agent = Column(String)                          # "support", "analyst", "writer", "voice", "orchestrator"
    action = Column(String)                         # "analyze_document", "generate_listing", etc.
    input_data = Column(JSON)
    output_data = Column(JSON, nullable=True)
    status = Column(String, default="pending")      # "pending", "running", "done", "error"
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
```

### Comportement des agents

**Agent Support (SupportAgent)** :
- Mène une conversation normal avec les prospect 24/7
- Reçoit un message utilisateur via WebSocket ou REST
- Extrait les critères de recherche du message (type, budget, surface, ville, critères spécifiques)
- Interroge la base vectorielle pour trouver les biens les plus proches sémantiquement et image/photos associé si possible/disponible
- Filtre ensuite par critères structurés (prix min/max, surface min, nombre de pièces) via SQL
- Formule une réponse naturelle présentant les biens trouvés avec prix, surface, points forts
- Si le prospect veut visiter : propose les créneaux disponibles via Google Calendar API
- Stocke la conversation et les critères dans PostgreSQL
- capable de capter/demander les information du prospect pour constitution dun CRM, suivi et relance plus tard
- Si confiance < 0.7 ou question hors scope : escalade vers l'agent humain via notification email/Slack
- Ton : professionnel mais chaleureux, adapté à l'immobilier. Tutoiement interdit. Toujours proposer une action suivante (visite, rappel, envoi de dossier).

**Agent Analyste (AnalystAgent)** :
- Reçoit un fichier (PDF) via l'API upload
- Classifie le type de document (DPE, PV d'AG copro, mandat, autre) via les premiers 500 tokens envoyés au LLM
- Selon le type, applique un prompt d'extraction spécifique qui retourne un JSON structuré
- Pour le DPE : classe énergétique, consommation, émissions CO2, recommandations
- Pour les charges copro : montant mensuel, travaux votés, fonds de travaux
- Stocke le JSON dans le champ extracted_data du Document
- Indexe le texte complet dans pgvector pour permettre des questions RAG ultérieures
- Traitement asynchrone via Celery (l'utilisateur n'attend pas)
- creation du bien et de ses information de base associé

**Agent Rédacteur (WriterAgent)** :
- Reçoit un property_id et une plateforme cible
- Charge les données du bien (Property) + les données extraites des documents associés (Document.extracted_data)
- Applique le template de la plateforme cible (longueur max, mots-clés SEO, format)
- Génère le titre + la description
- Stocke dans Listing avec status="draft"
- L'agent humain valide dans le dashboard avant publication
- Pour les emails : même logique mais avec des templates d'email (suivi visite, relance, nouveau bien correspondant)

**Agent Vocal (VoiceAgent) | VAPI.ai** :
- Connexion WebSocket bidirectionnelle
- Flux audio entrant → chunks de 3 secondes → Whisper API → texte
- Détection de fin de phrase (pause > 1.5 secondes)
- Le texte est envoyé au SupportAgent (même logique que le chatbot)
- La réponse texte est streamée vers le TTS (ElevenLabs API)
- Le flux audio de la réponse est renvoyé via WebSocket
- Pour le mode téléphonique : intégration Twilio (webhook d'appel entrant → WebSocket → même pipeline)
- Latence cible : < 2 secondes entre fin de parole utilisateur et début de réponse
- gere support client, prise de rdv, etc.. un peu comme l'agent support mais en vocal et avec une voix et un ton naturel

**Orchestrateur** :
- Utilise LangGraph pour définir des workflows comme des graphes d'états
- Chaque nœud du graphe est un appel à un agent ou un service externe
- Les transitions sont conditionnelles (si l'analyste trouve un DPE classe F → le rédacteur ajoute une mention dans l'annonce)
- État partagé entre les nœuds via un StateModel pydantic
- Workflows prédéfinis : new_property (nouveau bien → analyse docs → génération annonces → notification prospects), incoming_email (classification → réponse ou escalade), follow_up (relance automatique J+7 après visite)
- Les workflows peuvent être déclenchés par l'API, par n8n (webhook) ou par un cron (Celery beat)

### Configuration du tenant

Chaque agence a ses propres réglages stockés dans tenant.settings (JSON) :
```json
{
  "brand_voice": "professionnel et chaleureux",
  "default_greeting": "Bonjour, bienvenue chez ImmoPlus !",
  "escalation_email": "contact@immoplus.fr",
  "platforms": ["leboncoin", "seloger", "website"],
  "auto_followup_days": 7,
  "working_hours": {"start": "09:00", "end": "19:00"},
  "voice_enabled": true,
  "twilio_number": "+33123456789"
}
```

- Le dashbord doit permettre un paramettrage flexible des informations, des coordonné, agents,  pour chaque tenant pour lequel sera installer le systeme 

### Variables d'environnement (.env)

```
DATABASE_URL=postgresql://user:pass@localhost:5432/autopilot
REDIS_URL=redis://localhost:6379/0
CHROMA_PERSIST_DIR=./data/chroma
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+33...
SENDGRID_API_KEY=...
GOOGLE_CALENDAR_CREDENTIALS=./credentials.json
SECRET_KEY=...
ALLOWED_ORIGINS=http://localhost:3000,https://app.autopilot-immo.fr
```

### Docker Compose

```yaml

```

