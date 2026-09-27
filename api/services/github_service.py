import time
from datetime import datetime
import httpx
from fastapi import HTTPException

from api.core.config import settings
from api.schemas.project import ProjectListResponse, ProjectResponse

# Estrutura simples de cache em memória
_cache: dict[str, any] = {
    "data": None,
    "timestamp": 0.0
}


def _format_date(iso_date_str: str) -> str:
    """Converte formato ISO (2024-01-15T12:00:00Z) para DD/MM/AAAA."""
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return iso_date_str[:10]


async def fetch_github_repositories() -> ProjectListResponse:
    """
    Busca os repositórios públicos no GitHub, aplica cache em memória
    e valida o retorno através dos schemas Pydantic.
    """
    agora = time.time()
    
    # 1. Verifica se o cache ainda é válido
    if _cache["data"] is not None and (agora - _cache["timestamp"]) < settings.CACHE_TTL_SECONDS:
        return _cache["data"]

    # 2. Valida se o nome de usuário foi configurado
    if not settings.GITHUB_USERNAME:
        raise HTTPException(
            status_code=500,
            detail="GITHUB_USERNAME não configurado nas variáveis de ambiente."
        )

    url = f"https://api.github.com/users/{settings.GITHUB_USERNAME}/repos"
    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": 20
    }
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Portfolio-FastAPI-App"
    }
    
    # Adiciona autenticação apenas se o token existir no .env
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    # 3. Execução assíncrona da chamada HTTP
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Usuário do GitHub não encontrado.")
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erro ao consultar API do GitHub: {response.text}"
                )
            
            repos_data = response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Falha de conexão com o GitHub: {exc}")

    # 4. Filtra e mapeia para a lista de schemas tipados
    projects_list: list[ProjectResponse] = []
    
    for repo in repos_data:
        # Ignora forks para manter apenas repositórios próprios
        if repo.get("fork"):
            continue

        projects_list.append(
            ProjectResponse(
                id=repo["id"],
                name=repo["name"],
                description=repo.get("description"),
                html_url=repo["html_url"],
                homepage=repo.get("homepage"),
                language=repo.get("language") or "Geral",
                stars=repo.get("stargazers_count", 0),
                topics=repo.get("topics", []),
                updated_at=_format_date(repo.get("updated_at", ""))
            )
        )

    resultado = ProjectListResponse(
        total=len(projects_list),
        projects=projects_list
    )

    # 5. Atualiza o cache em memória
    _cache["data"] = resultado
    _cache["timestamp"] = agora

    return resultado