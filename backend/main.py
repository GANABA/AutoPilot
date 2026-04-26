import traceback
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import check_db_connection
from auth import login, verify_token
from schemas import LoginRequest, TokenResponse
from api.properties import router as properties_router
from api.leads import router as leads_router
from api.documents import router as documents_router
from api.listings import router as listings_router
from api.chat import router as chat_router
import redis as redis_lib

settings = get_settings()

app = FastAPI(
    title="AutoPilot Immo — POC",
    version="0.1.0",
    description="""
API backend du POC AutoPilot Immo — plateforme multi-agents pour agences immobilières.

## Authentification
1. **POST /api/auth/login** → récupère le `access_token`
2. Clique sur **Authorize** 🔒 (en haut à droite) et colle : `Bearer <token>`
3. Le token persiste entre les rechargements de page

## Agents
- **Agent Analyste** : upload un PDF → classification automatique (DPE / mandat / PV copro) + extraction structurée via GPT-4o-mini
""",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
    },
    openapi_tags=[
        {"name": "auth", "description": "Login et vérification du token JWT"},
        {"name": "properties", "description": "CRUD biens immobiliers"},
        {"name": "leads", "description": "CRUD prospects"},
        {"name": "documents", "description": "Upload PDF + analyse Agent Analyste"},
        {"name": "listings", "description": "Annonces générées par l'Agent Rédacteur (SeLoger, Leboncoin, PAP, site web)"},
        {"name": "chat", "description": "Agent Support — chatbot RAG + capture de leads"},
        {"name": "system", "description": "Health check"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties_router)
app.include_router(leads_router)
app.include_router(documents_router)
app.include_router(listings_router)
app.include_router(chat_router)


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": type(exc).__name__, "detail": str(exc), "trace": traceback.format_exc()},
    )


@app.get("/health", tags=["system"])
def health_check():
    db_ok = check_db_connection()

    redis_ok = False
    try:
        r = redis_lib.from_url(settings.redis_url, socket_connect_timeout=2)
        r.ping()
        redis_ok = True
    except Exception:
        pass

    return {
        "status": "ok" if db_ok and redis_ok else "degraded",
        "db": "connected" if db_ok else "error",
        "redis": "connected" if redis_ok else "error",
        "agency": settings.agency_name,
    }


@app.post(
    "/api/auth/login",
    response_model=TokenResponse,
    tags=["auth"],
    summary="Connexion admin",
    description="Retourne un JWT valide 24h. Utilise le token dans **Authorize** 🔒 pour les autres endpoints.",
)
def auth_login(body: LoginRequest):
    token = login(body.email, body.password)
    return TokenResponse(access_token=token)


@app.get(
    "/api/auth/me",
    tags=["auth"],
    summary="Profil du token courant",
)
def auth_me(payload: dict = Depends(verify_token)):
    return {"email": payload.get("sub"), "role": payload.get("role")}
