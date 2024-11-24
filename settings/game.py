from .pydantic_settings_config import config
from pydantic_settings import BaseSettings


class SpyGame(BaseSettings):
    model_config = config

    default_round_time: int = 6
    default_rounds: int = 5

    locations_limit: int = 24
