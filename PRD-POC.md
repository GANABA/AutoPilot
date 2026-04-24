# PRD — AutoPilot Immo · POC
## Preuve de Concept — Système Complet, Mono-Tenant, Low-Cost

> **Version :** 1.0  
> **Date :** Avril 2026  
> **Statut :** POC / Validation technique  
> **Modèle :** Mono-tenant (une seule agence configurée)  
> **Relation avec PRD.md :** Ce document est la version POC à développer en premier. Le `PRD.md` est la cible production multi-tenant à atteindre après validation.

---

## Objectif du POC

Valider en conditions réelles que les 5 agents IA fonctionnent correctement ensemble, que l'orchestration LangGraph tient la route, et que la proposition de valeur est réelle — sans se distraire par la complexité multi-tenant, la facturation, ou une infra coûteuse.

**Ce que le POC DOIT avoir :**
- Les 5 agents opérationnels (Support, Analyste, Rédacteur, Vocal, Orchestrateur)
- Un dashboard utilisable par une vraie agence
- Un widget chatbot embeddable sur un vrai site
- Un déploiement accessible en ligne (pas juste en local)

**Ce que le POC N'A PAS (intentionnellement) :**
- Multi-tenant / isolation de données entre agences
- Facturation / Stripe
- RBAC multi-rôles complexe (un seul compte admin suffit)
- RLS PostgreSQL
- Kubernetes
- CI/CD automatisé
- Monitoring production (Grafana, Prometheus)

---

## 1. Stack technique POC

### 1.1 LLM

| Usage | Modèle | Pourquoi |
|-------|--------|----------|
| Tâches complexes (rédaction, orchestration, analyse) | **GPT-4o** | Meilleure qualité, contexte long |
| Tâches simples (classification, extraction courte, support basique) | **GPT-4o-mini** | 15x moins cher que GPT-4o, latence <1s |
| Embeddings | **text-embedding-3-small** | Pas cher, bonne qualité pour le RAG |

> **Note de migration vers production :** Le switch vers Claude Sonnet 4.6 + Haiku 4.5 se fait en changeant le client LLM dans les agents (LangChain abstrait ça). Aucune refonte nécessaire.

### 1.2 Déploiement low-cost

| Brique | Solution POC | Coût | Solution prod (PRD.md) |
|--------|-------------|------|------------------------|
| **API backend** | **Railway** | ~$5/mois (usage-based) | Kubernetes (OVH/AWS) |
| **Base de données** | **Neon** (PostgreSQL + pgvector) | $0 (free tier 0.5GB) | AWS RDS Paris |
| **Redis / Queue** | **Upstash Redis** | $0 (free 10K cmd/jour) | Redis managé |
| **Worker Celery** | **Railway** (second service) | ~$2/mois | K8s pod dédié |
| **Frontend dashboard** | **Vercel** | $0 (free tier) | Vercel Pro ou S3+CDN |
| **Email** | **Resend** | $0 (3 000 emails/mois gratuits) | SendGrid |
| **Agent vocal** | **VAPI.ai** | $10 crédits offerts puis ~$0.05/min | VAPI.ai |
| **Téléphonie** | **Twilio** (numéro FR) | ~$1/mois + usage | Twilio |
| **Stockage fichiers** | **Cloudflare R2** | $0 (10GB gratuits) | AWS S3 |
| **Monitoring erreurs** | **Sentry** | $0 (free tier) | Sentry Team |

**Coût total estimé POC : 7-15 €/mois** (hors usage OpenAI et Twilio)

### 1.3 Stack complète POC

```
Backend  : Python 3.12, FastAPI, LangGraph, Celery
LLM      : OpenAI (GPT-4o + GPT-4o-mini + text-embedding-3-small)
DB       : PostgreSQL (Neon) + pgvector
Cache    : Redis (Upstash)
Voix     : VAPI.ai + Twilio
Email    : Resend
Fichiers : Cloudflare R2
Frontend : React 18 + Tailwind CSS (Vercel)
Widget   : JS Vanilla
Déploiement : Docker Compose (local) + Railway (cloud)
```

---

## 2. Architecture simplifiée

### 2.1 Vue d'ensemble

```
┌─────────────────────────────────────────────────────┐
│                    CLIENTS                          │
│  Site agence (widget JS) | Dashboard React          │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────┐
│              API FastAPI (Railway)                  │
│   Auth JWT simple | Config depuis .env              │
└──┬──────────┬────────────┬──────────────────────────┘
   │          │            │
┌──▼──┐  ┌───▼──┐  ┌──────▼──┐  ┌──────────────────┐
│Supp.│  │Anal. │  │Rédact.  │  │  Agent Vocal     │
│Agent│  │Agent │  │Agent    │  │  (VAPI.ai)       │
└──┬──┘  └───┬──┘  └──────┬──┘  └──────────────────┘
   │          │            │
┌──▼──────────▼────────────▼──────────────────────────┐
│          ORCHESTRATEUR (LangGraph)                  │
└──┬──────────┬────────────┬────────────────┬─────────┘
   │          │            │                │
┌──▼──┐  ┌───▼────┐  ┌────▼────┐  ┌────────▼──────┐
│Cely │  │pgvector│  │ OpenAI  │  │  Sentry       │
│+    │  │(Neon)  │  │  APIs   │  │  (erreurs)    │
│Redis│  └────────┘  └─────────┘  └───────────────┘
└──┬──┘
   │
┌──▼──────────────────────────────────────────────────┐
│         PostgreSQL — Neon (mono-tenant)             │
│   Pas de tenant_id — tables directes                │
└─────────────────────────────────────────────────────┘
```

### 2.2 Mono-tenant : ce que ça change concrètement

**Pas de `tenant_id` sur les tables.** Toutes les données appartiennent à l'agence configurée dans `.env`.

```python
# POC — requête directe, sans filtre tenant
def get_active_properties(db: Session) -> list[Property]:
    return db.query(Property).filter(Property.status == "active").all()

# Production (PRD.md) — filtre tenant systématique
def get_active_properties(db: Session, tenant_id: UUID) -> list[Property]:
    return db.query(Property).filter(
        Property.tenant_id == tenant_id,
        Property.status == "active"
    ).all()
```

**Auth simplifiée :** Un seul compte admin (email + mot de passe hashé), JWT pour le dashboard. Le widget chatbot utilise un token statique dans `.env`.

**Config agence dans `.env` directement** (pas de table `tenants`) :

```env
# Identité de l'agence
AGENCY_NAME="Agence ImmoPlus"
AGENCY_GREETING="Bonjour, bienvenue chez ImmoPlus !"
AGENCY_BRAND_VOICE="professionnel et chaleureux"
AGENCY_ESCALATION_EMAIL="contact@immoplus.fr"
AGENCY_WORKING_HOURS_START="09:00"
AGENCY_WORKING_HOURS_END="19:00"
WIDGET_TOKEN="tok_xxxxxxxxxxxx"

# LLM
OPENAI_API_KEY=sk-...
LLM_COMPLEX_MODEL=gpt-4o
LLM_SIMPLE_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Infrastructure
DATABASE_URL=postgresql://...@ep-xxx.neon.tech/autopilot
REDIS_URL=rediss://...@apn-xxx.upstash.io:6380
CLOUDFLARE_R2_BUCKET=autopilot-docs
CLOUDFLARE_R2_ACCESS_KEY=...

# Intégrations
VAPI_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+33...
RESEND_API_KEY=...
GOOGLE_CALENDAR_CREDENTIALS=./credentials.json

# App
SECRET_KEY=...
ADMIN_EMAIL=admin@immoplus.fr
ALLOWED_ORIGINS=https://immoplus.fr,https://dashboard-poc.vercel.app
```

---

## 3. Modèle de données simplifié

Sans `tenant_id`, sans `AuditLog` complet, sans `Notification` complexe.

```python
# models.py — version POC

class Property(Base):
    __tablename__ = "properties"
    id = Column(UUID, primary_key=True, default=uuid4)
    reference = Column(String)
    type = Column(String)                   # "appartement", "maison", "terrain"
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
    energy_class = Column(String, nullable=True)
    charges_monthly = Column(Float, nullable=True)
    photos = Column(JSON, default=[])       # URLs Cloudflare R2
    status = Column(String, default="active")  # "active", "under_offer", "sold"
    agent_name = Column(String, nullable=True)
    agent_email = Column(String, nullable=True)
    embedding = Column(Vector(1536), nullable=True)  # pgvector
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    criteria = Column(JSON, nullable=True)  # {type, budget_min, budget_max, surface_min, city}
    score = Column(Integer, default=0)
    status = Column(String, default="new")  # "new", "qualified", "visit_scheduled", "won", "lost"
    source = Column(String, nullable=True)  # "chatbot", "email", "phone"
    gdpr_consent = Column(Boolean, default=False)
    last_contact_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID, primary_key=True, default=uuid4)
    channel = Column(String)               # "chatbot", "email", "phone"
    lead_id = Column(UUID, ForeignKey("leads.id"), nullable=True)
    status = Column(String, default="open")  # "open", "qualified", "closed"
    messages = relationship("Message", back_populates="conversation")
    created_at = Column(DateTime, server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID, primary_key=True, default=uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"))
    role = Column(String)                  # "user", "assistant"
    content = Column(Text)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID, primary_key=True, default=uuid4)
    property_id = Column(UUID, ForeignKey("properties.id"), nullable=True)
    filename = Column(String)
    file_url = Column(String)              # URL Cloudflare R2
    doc_type = Column(String, nullable=True)  # "dpe", "copro", "mandat", "other"
    extracted_data = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # "pending", "processing", "done", "error"
    created_at = Column(DateTime, server_default=func.now())

class Listing(Base):
    __tablename__ = "listings"
    id = Column(UUID, primary_key=True, default=uuid4)
    property_id = Column(UUID, ForeignKey("properties.id"))
    platform = Column(String)              # "seloger", "leboncoin", "website"
    title = Column(String)
    content = Column(Text)
    status = Column(String, default="draft")  # "draft", "approved"
    created_at = Column(DateTime, server_default=func.now())

class Visit(Base):
    __tablename__ = "visits"
    id = Column(UUID, primary_key=True, default=uuid4)
    property_id = Column(UUID, ForeignKey("properties.id"))
    lead_id = Column(UUID, ForeignKey("leads.id"))
    scheduled_at = Column(DateTime)
    status = Column(String, default="scheduled")  # "scheduled", "done", "cancelled", "no_show"
    feedback_prospect = Column(Text, nullable=True)
    calendar_event_id = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID, primary_key=True, default=uuid4)
    agent = Column(String)                 # "support", "analyst", "writer", "voice", "orchestrator"
    action = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON, nullable=True)
    status = Column(String, default="pending")  # "pending", "running", "done", "error"
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
```

---

## 4. Les 5 agents — comportement POC

Même comportement que dans le `PRD.md`, avec ces simplifications :

### Agent Support
- Identique au PRD.md — chatbot 24/7, extraction critères, RAG + SQL, Calendar
- Config chargée depuis `.env` (pas depuis table `tenants`)
- Escalade par email via Resend (pas SendGrid)

### Agent Analyste
- Identique au PRD.md — classification PDF, extraction DPE/mandat/PV copro
- Fichiers stockés sur Cloudflare R2 (pas AWS S3)
- Celery task sur Upstash Redis

### Agent Rédacteur
- Identique au PRD.md — génération annonces par plateforme, workflow draft → validation
- Plateforme par défaut : SeLoger, LeBonCoin, site agence

### Agent Vocal (VAPI.ai)
- Identique au PRD.md — appels entrants Twilio → VAPI → pipeline → Calendar
- Config voix dans `.env` (voice_id ElevenLabs ou voix VAPI native)

### Orchestrateur (LangGraph)
- Identique au PRD.md — workflows `new_property`, `incoming_email`, `follow_up`
- Déclenché par API, Celery beat (cron), ou webhook

---

## 5. Structure du projet

```
autopilot-immo-poc/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Chargement .env → settings
│   ├── database.py                # Connexion Neon PostgreSQL
│   ├── models.py                  # SQLAlchemy models (sans tenant_id)
│   ├── agents/
│   │   ├── support_agent.py       # Agent Support (LangGraph node)
│   │   ├── analyst_agent.py       # Agent Analyste
│   │   ├── writer_agent.py        # Agent Rédacteur
│   │   ├── voice_agent.py         # Webhook VAPI.ai
│   │   └── orchestrator.py        # LangGraph workflows
│   ├── api/
│   │   ├── properties.py          # CRUD biens
│   │   ├── leads.py               # CRUD leads
│   │   ├── conversations.py       # Conversations + messages
│   │   ├── documents.py           # Upload + analyse docs
│   │   ├── listings.py            # Annonces générées
│   │   ├── visits.py              # Visites
│   │   └── auth.py                # Login JWT (compte unique)
│   ├── services/
│   │   ├── llm.py                 # Client OpenAI (GPT-4o / 4o-mini)
│   │   ├── embeddings.py          # text-embedding-3-small
│   │   ├── vector_store.py        # pgvector queries
│   │   ├── calendar.py            # Google Calendar
│   │   ├── email.py               # Resend
│   │   └── storage.py             # Cloudflare R2
│   ├── worker.py                  # Celery worker
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx      # Vue principale
│   │   │   ├── Properties.tsx     # Gestion biens
│   │   │   ├── Leads.tsx          # CRM prospects
│   │   │   ├── Conversations.tsx  # Historique chats
│   │   │   ├── Listings.tsx       # Validation annonces
│   │   │   └── Settings.tsx       # Config agence
│   │   └── components/
├── widget/
│   └── chatbot.js                 # Widget embeddable (JS Vanilla)
├── docker-compose.yml             # Dev local complet
├── railway.toml                   # Config déploiement Railway
└── .env.example
```

---

## 6. Déploiement

### Local (développement)

```yaml
# docker-compose.yml
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [redis]

  worker:
    build: ./backend
    command: celery -A worker worker --loglevel=info
    env_file: .env
    depends_on: [redis]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  # PostgreSQL en local (Neon en prod)
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: autopilot
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports: ["5432:5432"]
```

```bash
docker compose up        # Lance tout en local
docker compose up api    # API seulement
```

### Cloud (POC en ligne)

**Railway** — déploiement en 3 clics depuis GitHub :

```toml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "backend/Dockerfile"

[[services]]
name = "api"
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"

[[services]]
name = "worker"
startCommand = "celery -A worker worker --loglevel=info"
```

**Vercel** — frontend React :
```bash
vercel deploy  # depuis le dossier frontend/
```

**Neon** — base de données :
```bash
# Migration initiale
alembic upgrade head

# pgvector extension (à activer une fois dans Neon console)
CREATE EXTENSION IF NOT EXISTS vector;
```

**Coût total POC en ligne :**

| Service | Coût/mois |
|---------|-----------|
| Railway (API + Worker) | 0 € (30j gratuits) puis 1 $/mois |
| Neon PostgreSQL | 0 € (free tier) |
| Upstash Redis | 0 € (free tier) |
| Vercel (frontend) | 0 € |
| Cloudflare R2 (fichiers) | 0 € (< 10 GB) |
| Resend (email) | 0 € (< 3 000/mois) |
| **Total infra** | **~7 €/mois** |
| OpenAI (usage) | 5-20 € selon volume de tests |
| VAPI.ai (vocal) | 0 € (crédits offerts) |
| Twilio (numéro FR) | ~1 € |
| **Total all-in** | **~13-28 €/mois** |

---

## 7. Roadmap POC

| Semaine | Livrables |
|---------|-----------|
| 1 | Setup projet, Docker Compose, FastAPI + PostgreSQL (Neon) + pgvector, auth JWT simple |
| 2 | Modèles de données, CRUD biens, upload fichiers (R2), indexation embeddings |
| 3 | Agent Analyste : classification PDF, extraction DPE + mandat + PV copro, Celery async |
| 4 | Agent Rédacteur : génération annonces SeLoger/LeBonCoin/website, workflow draft |
| 5 | Agent Support : chatbot web, RAG + SQL, Google Calendar, widget JS |
| 6 | Agent Vocal : webhook VAPI.ai, intégration Twilio, tests appels entrants |
| 7 | Orchestrateur LangGraph : workflows `new_property` + `follow_up` + `incoming_email` |
| 8 | Dashboard React minimal (biens, leads, conversations, validation annonces) |
| 9 | Déploiement Railway + Vercel, tests end-to-end avec une vraie agence |
| 10 | Corrections, polish, documentation, bilan → go/no-go vers version production |

**Critères de succès du POC :**
- Les 5 agents répondent correctement sur des cas réels
- Une agence pilote utilise le chatbot sur son vrai site pendant 2 semaines
- Au moins 10 leads qualifiés automatiquement sans intervention humaine
- L'analyste extrait correctement les données de 10 PDFs réels (DPE, mandats)
- L'agent vocal décroche et qualifie un appel entrant de bout en bout

---

## 8. Chemin vers la production (PRD.md)

Une fois le POC validé, la migration vers la version production (`PRD.md`) se fait par étapes :

| Changement | Effort | Impact |
|-----------|--------|--------|
| Ajouter `tenant_id` sur toutes les tables | ~1 jour | Migration Alembic + filtres dans les repositories |
| Activer RLS PostgreSQL | ~2h | Non-breaking si tenant_id déjà en place |
| Passer de `.env` config à table `tenants` | ~1 jour | Déplacer settings JSON dans la DB |
| Switch LLM OpenAI → Claude Sonnet/Haiku | ~2h | LangChain abstrait le provider |
| Railway → Kubernetes (OVH/AWS) | ~3 jours | Helm charts, ingress, HPA |
| Neon free → RDS Paris | ~1h | Changer DATABASE_URL |
| Auth mono-user → RBAC multi-rôles | ~2 jours | Nouveau système de permissions |
| Resend → SendGrid | ~1h | Changer client email |
| Stripe billing | ~3 jours | Plans + webhooks + limites par plan |

> Le POC est conçu pour que chaque migration vers prod soit un ajout, pas une réécriture.

---

*Référence production : voir `PRD.md` (v1.1)*
