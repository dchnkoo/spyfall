from .pydantic_settings_config import config
from pydantic_settings import BaseSettings
import pydantic as _p


class Bot(BaseSettings):
    model_config = config

    token: str = _p.Field(..., alias="bot_token")
