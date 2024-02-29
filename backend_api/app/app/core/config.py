import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 10 #this is 10 minutes
    ACCESS_TOKEN_EXPIRE_SECONDS: int = (
            60 * 10 * 60
    )  # this is 10 hours used while developing
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 24 * 60 * 60
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}

    # POSTGRES
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # TESTS POSTGRES
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # GOOGLE OAUTH CREDENTIALS
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # COINMARKETCAP
    COINMARKETCAP_KEY:str
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection_tests(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("TEST_POSTGRES_USER"),
            password=values.get("TEST_POSTGRES_PASSWORD"),
            host=values.get("TEST_POSTGRES_SERVER"),
            path=f"/{values.get('TEST_POSTGRES_DB') or ''}",
        )

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:8080",
        "http://localhost",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = "local.env"
        env_file_encoding = "utf-8"


settings = Settings()
print(settings.SQLALCHEMY_DATABASE_URI)
