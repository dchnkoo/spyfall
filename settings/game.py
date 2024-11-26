from .pydantic_settings_config import config
from pydantic_settings import BaseSettings


class SpyGame(BaseSettings):
    model_config = config

    default_round_time: int = 6
    default_rounds: int = 5

    locations_limit: int = 24
    roles_limit: int = 11
    role_description_limit: int = 300

    min_round_time: int = 3
    max_round_time: int = 10

    min_rounds: int = 3
    max_rounds: int = 10

    max_players_in_room: int = 12

    recruitment_time: int = 60
    recruitment_edit_interval: int = 5
