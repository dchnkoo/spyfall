from aiogram.utils.markdown import markdown_decoration
from aiogram.exceptions import TelegramForbiddenError
from aiogram import enums as aiogram_enums, types
from aiogram.client.default import Default

from urllib.parse import urlparse

from utils.requests import async_request_session
from utils.chat.model import ChatModel

from spy.routers import spybot

from caching import CacheModel, CachePrefix

from settings import spygame, redis

from . import enums, bases

import sqlmodel as _sql
import pydantic as _p
import typing as _t


model_config = _p.ConfigDict(
    str_strip_whitespace=True,
    validate_assignment=True,
    validate_default=True,
    use_enum_values=True,
    extra="ignore",
    frozen=False,
)


class BaseModel(_p.BaseModel):
    model_config = model_config

    @staticmethod
    def markdown_string(field: str):
        return markdown_decoration.quote(field)


class TelegramUserModel(BaseModel, types.User, ChatModel, CacheModel[int]):
    model_config = model_config

    db: _t.ClassVar[int] = redis.users_db
    cache_prefix: _t.ClassVar[str] = CachePrefix.user
    cache_live_time: _t.ClassVar[int] = 2 * 24 * 60 * 60

    id: int = _sql.Field(sa_type=_sql.BigInteger, primary_key=True)

    @property
    def escaped_first_name(self):
        return self.markdown_string(self.first_name)

    @property
    def escaped_last_name(self):
        if self.last_name:
            return self.markdown_string(self.last_name)

    @property
    def escaped_full_name(self):
        if self.last_name:
            return f"{self.escaped_first_name} {self.escaped_last_name}"
        return self.escaped_first_name

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

    async def send_message(
        self,
        text: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        parse_mode: str | Default | None = aiogram_enums.ParseMode.MARKDOWN_V2,
        entities: list[types.MessageEntity] | None = None,
        link_preview_options: types.LinkPreviewOptions | Default | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | Default | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: types.ReplyParameters | None = None,
        reply_markup: (
            types.InlineKeyboardMarkup
            | types.ReplyKeyboardMarkup
            | types.ReplyKeyboardRemove
            | types.ForceReply
            | None
        ) = None,
        allow_sending_without_reply: bool | None = None,
        disable_web_page_preview: bool | Default | None = None,
        reply_to_message_id: int | None = None,
        request_timeout: int | None = None,
        **action_kw,
    ) -> types.Message:
        try:
            return await super(TelegramUserModel, self).send_message(
                text,
                business_connection_id,
                message_thread_id,
                parse_mode,
                entities,
                link_preview_options,
                disable_notification,
                protect_content,
                allow_paid_broadcast,
                message_effect_id,
                reply_parameters,
                reply_markup,
                allow_sending_without_reply,
                disable_web_page_preview,
                reply_to_message_id,
                request_timeout,
                **action_kw,
            )
        except TelegramForbiddenError:
            pass

    def __eq__(self, other: "TelegramUserModel") -> bool:
        assert other is TelegramUserModel or issubclass(
            other.__class__, TelegramUserModel
        ), "It's not subclass or class of TelegramUserModel"
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class PackageModel(BaseModel, bases.Name, bases.PrimaryKey):
    scope: enums.PackageScope = enums.PackageScope.PRIVATE
    type: enums.PackageType = enums.PackageType.USER

    @property
    def escaped_name(self):
        return self.markdown_string(self.name)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: "PackageModel") -> bool:
        assert other is PackageModel or issubclass(
            other.__class__, PackageModel
        ), "It's not subclass or class of PackageModel"
        return self.name == other.name


class LocationModel(BaseModel, bases.Name, bases.PrimaryKey):

    image_url: _t.Optional[str] = None

    @property
    def escaped_name(self):
        return self.markdown_string(self.name)

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
            if res.status_code not in range(100, 400):
                raise ValueError("Not valid image.")

        content_type: str = res.headers.get("content-type", None)
        if content_type is None:
            raise ValueError("Not valid image.")
        return content_type.startswith("image")

    def __eq__(self, other: "LocationModel") -> bool:
        assert other is LocationModel or issubclass(
            other.__class__, LocationModel
        ), "It's not subclass or class of Location model"
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class RoleModel(BaseModel, bases.Name, bases.PrimaryKey):

    description: _t.Optional[str] = None
    _is_spy: bool = _p.PrivateAttr(default=False)

    @property
    def escaped_name(self):
        return self.markdown_string(self.name)

    @property
    def escaped_description(self):
        if self.description:
            return self.markdown_string(self.description)
        return ""

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
            name="Шпигун",
            description="Ти шпигун! Твоя ціль дізнатися локацію.",
        )
        role.is_spy = True
        return role

    @_p.field_validator("description", mode="before")
    def validate_description(cls, v: str):
        if v is not None:
            assert len(v) <= spygame.role_description_limit
        return v

    def __eq__(self, other: "RoleModel") -> bool:
        assert other is RoleModel or issubclass(
            other.__class__, RoleModel
        ), "It's not subclass or class of RoleModel"
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
