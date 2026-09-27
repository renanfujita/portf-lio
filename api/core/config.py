import os
from pathlib import Path
from dotenv import load_dotenv

# Determina o caminho raiz do projeto (sobe de api/core até meu-portfolio/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Carrega as variáveis declaradas no arquivo .env se ele existir localmente
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    PROJECT_NAME: str = "Portfolio API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Credenciais e integrações
    GITHUB_USERNAME: str = os.getenv("GITHUB_USERNAME", "")
    GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN") or None
    
    # TTL (Time-To-Live) do cache em memória em segundos (padrão: 1 hora)
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

# Instância pronta para uso em outros módulos
settings = Settings()