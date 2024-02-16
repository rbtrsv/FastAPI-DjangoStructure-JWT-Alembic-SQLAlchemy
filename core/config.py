import secrets
from datetime import timedelta
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr, validator

class Settings(BaseSettings):
    # Basic application settings
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    PROJECT_NAME: str = "Company Name FastAPI"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "An awesome project."
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database settings
    # DATABASE_URL: str = "postgresql+asyncpg://rbtrsv:zkykbPeSIPht42zxYeSzUOCDKAjlXQ9r@dpg-cn70u721hbls73a0vce0-a.frankfurt-postgres.render.com/finpydb"
    DATABASE_URL: str = "postgresql+asyncpg://rbtrsv:somepass123@localhost:5433/finpy_api_db"

    # Authentication settings
    JWT_SIGNING_KEY: str = '+xn7i)5xjxups-@_9&rep0l4^ix6p0!0z9pqr@!^*qz+0233f('
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION: timedelta = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRATION: timedelta = timedelta(days=7)

    # CORS configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, list):
            return v
        raise ValueError("Invalid BACKEND_CORS_ORIGINS format")

    # SMTP settings (all optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_ENABLED: bool = False

    # Sentry DSN (optional)
    SENTRY_DSN: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
