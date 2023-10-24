from enum import Enum, unique
from typing import Any, Dict, List

from fastapi.security import OAuth2PasswordBearer
from pydantic import NonNegativeInt, PositiveInt
from pydantic_settings import BaseSettings as pyBaseSettings
from pydantic_settings import SettingsConfigDict

from family.utils.password import get_password_hash


@unique
class Environment(str, Enum):
    local = "local"
    development = "development"
    qa = "qa"
    production = "production"


class BaseSettings(pyBaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    environment: str = Environment.development


class AppSettings(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    api_title: str = "API Family-Tree"
    srv_title: str = "SRV Family-Tree"
    version: str = "0.0.1"
    description: str = "Backend Family-Tree service 💬"

    max_connection_count: int = 10
    min_connection_count: int = 10

    api_prefix: str = "/api/family"
    srv_prefix: str = "/srv/family"

    allowed_hosts: List[str] = ["*"]

    routes_nolog: list = [  # ручки которые не логируются мидлварью
        "/docs",
        "/openapi.json",
        "/v1/healthcheck",
        "/v1/accounts/login",
    ]

    @property
    def base_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "version": self.version,
            "description": self.description,
            "on_startup": [],
            "on_shutdown": [],
        }

    @property
    def api_kwargs(self) -> Dict[str, Any]:
        api_kw = {
            "docs_url": self.api_prefix + self.docs_url,
            "openapi_url": self.api_prefix + self.openapi_url,
            "redoc_url": self.api_prefix + self.redoc_url,
            # "openapi_tags": api_tags_metadata,
            "title": self.api_title,
        }
        api_kw.update(self.base_kwargs)
        return api_kw

    @property
    def srv_kwargs(self) -> Dict[str, Any]:
        srv_kw = {
            "title": self.srv_title,
            "docs_url": self.srv_prefix + self.docs_url,
            "openapi_url": self.srv_prefix + self.openapi_url,
            "redoc_url": self.srv_prefix + self.redoc_url,
            # "openapi_tags": srv_tags_metadata,
        }
        srv_kw.update(self.base_kwargs)
        return srv_kw

    @property
    def pass_routes(self):
        """Ендпоинты, которые можно не логировать.

        Returns:
            str
        """
        return [f"{self.api_prefix}{url}" for url in self.routes_nolog]


class ServerSettings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: PositiveInt = 8010
    debug: bool = True


class DatabaseSettings(BaseSettings):
    dialect: str = "postgresql"

    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    echo: bool = False

    db_pool_min_size: PositiveInt = 1
    db_pool_max_size: PositiveInt = 1

    statement_cache_size: NonNegativeInt = 0  # 0 to work with transaction_pooling

    @property
    def _uri(self):
        db_name = self.db_name
        return f"{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{db_name}"

    @property
    def dsn_no_driver(self) -> str:
        return f"{self.dialect}://{self._uri}"

    @property
    def dsn(self) -> str:
        return f"{self.dialect}+asyncpg://{self._uri}"


class JWTSettings(BaseSettings):
    SECRET_KEY: str = (
        "06fc53c2b88753232b1060b644f05e2165d364977d226775616ea6330c0189b96c"
    )
    ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def token_expire(self) -> int:
        if self.environment == Environment.local:
            return 1440  # 24 hours

        return self.ACCESS_TOKEN_EXPIRE_MINUTES

    model_config = SettingsConfigDict(env_prefix="jwt_")


class AdminSettings(BaseSettings):
    login: str = "admin"
    password: str = "admin"
    email: str = "admin@domain.com"

    model_config = SettingsConfigDict(env_prefix="superadmin_")

    @property
    def credentials(self):
        return {
            "username": self.login,
            "hashed_password": get_password_hash(self.password),
            "email": self.email,
            "is_enabled": True,
            "role_uuid": None,
        }


db_settings = DatabaseSettings()
server_settings = ServerSettings()
app_settings = AppSettings()
jwt_settings = JWTSettings()
admin_settings = AdminSettings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=app_settings.api_prefix + "/v1/accounts/login",
)
