from .pydantic_settings_config import config
from pydantic_settings import BaseSettings
import pydantic as _p

import typing as _t


class Postgres(BaseSettings):
    model_config = config
    key: _t.ClassVar[str] = "postgres"

    host: str = _p.Field("localhost", alias=key + "_host")
    port: int = _p.Field(5432, alias=key + "_port")
    user: str = _p.Field(key, alias=key + "_user")
    password: str = _p.Field(key, alias=key + "_password")
    db: str = _p.Field(key, alias=key + "_db")

    @property
    def dsn(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def async_dsn(self):
        return self.dsn.replace("postgresql", "postgresql+asyncpg")
