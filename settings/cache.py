from .pydantic_settings_config import config
from pydantic_settings import BaseSettings
import pydantic as _p

import datetime as _date

import typing as _t


class Redis(BaseSettings):
    model_config = config

    host: str = _p.Field("localhost", alias="redis_host")
    port: int = _p.Field(6379, alias="redis_port")
    db: int = _p.Field(0, alias="redis_db")
    password: str = _p.Field("", alias="redis_password")
    username: str = _p.Field("", alias="redis_user")

    @property
    def default_cache_live_time(self):
        return (
            ((now := _date.datetime.now(_date.timezone.utc)) + _date.timedelta(hours=5))
            - now
        ).seconds

    @property
    def users_db(self):
        return self.db + 1

    @property
    def game_db(self):
        return self.users_db + 1

    @property
    def states_db(self):
        return self.game_db + 1

    def dsn(self, db: _t.Optional[int] = None):
        return f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{db or self.db}"
