from datetime import datetime
from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    """Contrato que representa um repositório formatado para o portfólio."""
    id: int = Field(..., description="ID único do repositório no GitHub")
    name: str = Field(..., description="Nome do projeto/repositório")
    description: str | None = Field(None, description="Descrição detalhada do projeto")
    html_url: str = Field(..., description="Link público do repositório no GitHub")
    homepage: str | None = Field(None, description="Link de demonstração do projeto no ar (se houver)")
    language: str | None = Field("Diversos", description="Linguagem principal detectada")
    stars: int = Field(0, description="Quantidade de estrelas recebidas")
    topics: list[str] = Field(default_factory=list, description="Tópicos/tags associadas no GitHub")
    updated_at: str = Field(..., description="Data da última atualização em formato legível")


class ProjectListResponse(BaseModel):
    """Contrato da resposta do endpoint de listagem de projetos."""
    total: int = Field(..., description="Quantidade total de projetos retornados")
    projects: list[ProjectResponse] = Field(..., description="Lista de projetos formatados")