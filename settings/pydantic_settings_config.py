from pydantic_settings import SettingsConfigDict
from .pathes import ROOT_DIR


config = SettingsConfigDict(
    str_strip_whitespace=True,
    use_enum_values=True,
    frozen=True,
    validate_default=True,
    env_file=ROOT_DIR / ".env",
    extra="ignore",
)
