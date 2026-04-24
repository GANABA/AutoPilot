from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import check_db_connection
from auth import login, verify_token
from schemas import LoginRequest, TokenResponse
from api.properties import router as properties_router
from api.leads import router as leads_router
from api.documents import router as documents_router
import redis as redis_lib

settings = get_settings()

app = FastAPI(
    title="AutoPilot Immo — POC",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
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


@app.post("/api/auth/login", response_model=TokenResponse, tags=["auth"])
def auth_login(body: LoginRequest):
    token = login(body.email, body.password)
    return TokenResponse(access_token=token)


@app.get("/api/auth/me", tags=["auth"])
def auth_me(payload: dict = Depends(verify_token)):
    return {"email": payload.get("sub"), "role": payload.get("role")}
