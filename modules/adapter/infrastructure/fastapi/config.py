import os

from pydantic import BaseSettings
from urllib.parse import quote as urlquote


class Config(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"

    # Uvicorn
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    RELOAD: bool = False

    # Sqlalchemy
    DATA_WAREHOUSE_URL: str = "sqlite+aiosqlite:///:memory:"
    DATA_LAKE_URL: str = "sqlite+aiosqlite:///:memory:"
    DB_ECHO: bool = True
    DB_PRE_PING: bool = True

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_NODE_HOST_1: str | None = os.environ.get("REDIS_NODE_HOST_1")
    REDIS_NODE_HOST_2: str | None = os.environ.get("REDIS_NODE_HOST_2")

    # Jwt
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "hawaii"
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHMS") or "HS256"

    # Celery
    # BACKEND_RESULT = "db+mysql+pymysql://antgirl:1234@localhost:3306/antgirl"
    BACKEND_RESULT = "db+mysql+pymysql://apartalk_admin:!wjstngks117@localhost:3306/apartalk_data_lake"
    TIMEZONE = "Asia/Seoul"
    CELERY_ENABLE_UTC = False

    class Config:
        validate_assignment = True


class LocalConfig(Config):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "!xhemgha@#%2214"
    DATA_LAKE_URL: str = os.getenv(
        "DEV_DATA_LAKE_URL",
        "mysql+pymysql://apartalk_admin:!wjstngks117@localhost:3306/apartalk_data_lake",
    )
    DATA_WAREHOUSE_URL: str = os.getenv(
        "DEV_WAREHOUSE_URL",
        "mysql+pymysql://apartalk_admin:!wjstngks117@localhost:3306/apartalk_data_warehouse",
    )


class TestConfig(Config):
    ENV: str = "testing"
    TESTING: bool = True
    RELOAD: bool = True


class DevelopmentConfig(Config):
    ENV: str = "development"
    DATA_LAKE_URL: str = os.getenv("DEV_DATA_LAKE_URL", "sqlite+aiosqlite:///:memory:")
    DATA_WAREHOUSE_URL: str = os.getenv(
        "DEV_DATA_WAREHOUSE_URL", "sqlite+aiosqlite:///:memory:"
    )

    RELOAD: bool = True
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_KEY: str | None = os.getenv("SENTRY_KEY")


class ProductionConfig(Config):
    ENV: str = "production"
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None

    # Sqlalchemy
    DATA_LAKE_URL: str | None = os.getenv("PROD_DATA_LAKE_URL")
    DATA_WAREHOUSE_URL: str | None = os.getenv("PROD_DATA_WAREHOUSE_URL")

    # Sentry
    SENTRY_ENVIRONMENT: str = "production"
    SENTRY_KEY: str | None = os.getenv("SENTRY_KEY")


def get_config() -> Config:

    env: str = os.getenv("FASTAPI_ENV", "local")

    config_type: dict = dict(
        default=LocalConfig,
        local=LocalConfig,
        testing=TestConfig,
        development=DevelopmentConfig,
        production=ProductionConfig,
    )

    result = config_type.get(env)

    return result()


fastapi_config: Config = get_config()
