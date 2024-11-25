from aiogram.types import User

from urllib.parse import urlparse

from utils.requests import async_request_session
from utils.chat.model import ChatModel

from spy.routers import spybot

from caching import CacheModel, CachePrefix

from settings import spygame

from . import enums, bases

import sqlmodel as _sql
import pydantic as _p
import typing as _t
import json


model_config = _p.ConfigDict(
    use_enum_values=True,
    str_strip_whitespace=True,
    validate_default=True,
    extra="ignore",
    frozen=False,
)


class TelegramUserModel(User, ChatModel, CacheModel[int]):
    model_config = model_config

    cache_prefix: _t.ClassVar[str] = CachePrefix.user
    cache_live_time: _t.ClassVar[int] = 2 * 24 * 60 * 60

    id: int = _sql.Field(sa_type=_sql.BigInteger, primary_key=True)

    @property
    def cache_identity(self):
        return self.id

    @property
    def chat_id(self):
        return self.id

    @property
    def __bot__(self):
        return spybot

    @property
    def language(self):
        if not self.language_code:
            return "en"
        return self.language_code

    def __eq__(self, other: "TelegramUserModel") -> bool:
        assert other is TelegramUserModel or issubclass(
            other.__class__, TelegramUserModel
        )
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class PackageModel(_p.BaseModel, bases.Name, bases.PrimaryKey):
    model_config = model_config

    scope: enums.PackageScope = enums.PackageScope.PRIVATE
    type: enums.PackageType = enums.PackageType.USER

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "PackageModel") -> bool:
        assert other is PackageModel or issubclass(other.__class__, PackageModel)
        return self.name == other.name


class LocationModel(_p.BaseModel, bases.Name, bases.PrimaryKey):
    model_config = model_config

    image_url: _t.Optional[str] = None

    @_p.field_validator("image_url", mode="before")
    @classmethod
    def validate_image_url(cls, v: str):
        if v is not None:
            parsed_url = urlparse(v)
            assert all((parsed_url.scheme, parsed_url.netloc, parsed_url.path))
        return v

    @classmethod
    async def check_if_image_valid(cls, url: str) -> bool:
        cls.validate_image_url(url)

        async with async_request_session() as client:
            res = await client.get(url)
            assert res.status_code == 200

        content_type: str = res.headers.get("content-type", None)
        assert content_type is not None
        return content_type.startswith("image")

    def __eq__(self, other: "LocationModel") -> bool:
        assert other is LocationModel or issubclass(other.__class__, LocationModel)
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class RoleModel(_p.BaseModel, bases.Name, bases.PrimaryKey):
    model_config = model_config

    description: _t.Optional[str] = None
    _is_spy: bool = _p.PrivateAttr(default=False)

    @_p.computed_field
    @property
    def is_spy(self) -> bool:
        return self._is_spy

    @is_spy.setter
    def is_spy(self, value: bool):
        assert isinstance(value, bool)
        self._is_spy = value

    @staticmethod
    def get_spy_role():
        role = RoleModel(
            name="Spy",
            description="You are a spy! Your goal is to guess the location.",
        )
        role.is_spy = True
        return role

    @_p.field_validator("description", mode="before")
    def validate_description(cls, v: str):
        if v is not None:
            assert len(v) <= spygame.role_description_limit
        return v

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: _t.Any | None = None,
    ):
        data = json.loads(json_data)
        validated = cls.__pydantic_validator__.validate_python(
            data, strict=strict, context=context
        )
        validated.is_spy = data["is_spy"]
        return validated

    def __eq__(self, other: "RoleModel") -> bool:
        assert other is RoleModel or issubclass(other.__class__, RoleModel)
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
