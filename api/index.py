from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.core.config import settings
from api.routers import projects

# Instância central do FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API de backend para entrega de telemetria e dados de projetos do portfólio.",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Rotas da API
app.include_router(projects.router)


@app.get(
    "/api/health",
    tags=["Monitoramento"],
    summary="Health Check da API"
)
async def health_check():
    """Endpoint simples para monitorar se a API serverless está ativa."""
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }


# Suporte local: serve os ficheiros estáticos da pasta public/
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
if PUBLIC_DIR.exists():
    app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static_frontend")