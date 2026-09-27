from fastapi import APIRouter
from api.schemas.project import ProjectListResponse
from api.services.github_service import fetch_github_repositories

router = APIRouter(
    prefix="/api/projects",
    tags=["Projetos"]
)


@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="Listar projetos do portfólio",
    description="Retorna os repositórios públicos atualizados do GitHub utilizando cache em memória."
)
async def get_projects():
    """
    Endpoint assíncrono que consulta a camada de serviços
    e devolve os projetos devidamente tipados e filtrados.
    """
    return await fetch_github_repositories()