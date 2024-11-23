from abc import ABC, abstractmethod

from contextlib import asynccontextmanager
from functools import partial

from aiogram.utils.chat_action import ChatActionSender
from aiogram.client.default import Default
from aiogram.enums import ChatAction
from aiogram import Bot, types

import typing as _t


class ChatModel(ABC):

    @property
    @abstractmethod
    def chat_id(self): ...

    @property
    @abstractmethod
    def __bot__(self) -> Bot: ...

    @asynccontextmanager
    async def chat_action(self, action: ChatAction = ChatAction.TYPING, **kw):
        async with ChatActionSender(
            bot=self.__bot__,
            chat_id=self.chat_id,
            action=action,
            **kw,
        ):
            yield

    @property
    def create_chat_invite_link(self):
        return partial(self.__bot__.create_chat_invite_link, chat_id=self.chat_id)

    @property
    def delete_message(self):
        return partial(
            self.__bot__.delete_message,
            chat_id=self.chat_id,
        )

    @property
    def delete_messages(self):
        return partial(
            self.__bot__.delete_messages,
            chat_id=self.chat_id,
        )

    @property
    def edit_message_caption(self):
        return partial(
            self.__bot__.edit_message_caption,
            chat_id=self.chat_id,
        )

    @property
    def edit_message_reply_markup(self):
        return partial(self.__bot__.edit_message_reply_markup, chat_id=self.chat_id)

    @property
    def edit_message_text(self):
        return partial(self.__bot__.edit_message_text, chat_id=self.chat_id)

    @property
    def get_chat(self):
        return partial(
            self.__bot__.get_chat,
            chat_id=self.chat_id,
        )

    @property
    def get_chat_administrators(self):
        return partial(
            self.__bot__.get_chat_administrators,
            chat_id=self.chat_id,
        )

    @property
    def get_chat_member(self):
        return partial(
            self.__bot__.get_chat_member,
            chat_id=self.chat_id,
        )

    @property
    def get_chat_member_count(self):
        return partial(
            self.__bot__.get_chat_member_count,
            chat_id=self.chat_id,
        )

    @property
    def leave_chat(self):
        return partial(
            self.__bot__.leave_chat,
            chat_id=self.chat_id,
        )

    @property
    def pin_chat_message(self):
        return partial(
            self.__bot__.pin_chat_message,
            chat_id=self.chat_id,
        )

    async def send_message(
        self,
        text: str,
        business_connection_id: _t.Optional[str] = None,
        message_thread_id: _t.Optional[int] = None,
        parse_mode: _t.Optional[_t.Union[str, Default]] = Default("parse_mode"),
        entities: _t.Optional[list[types.MessageEntity]] = None,
        link_preview_options: _t.Optional[
            _t.Union[types.LinkPreviewOptions, Default]
        ] = Default("link_preview"),
        disable_notification: _t.Optional[bool] = None,
        protect_content: _t.Optional[_t.Union[bool, Default]] = Default(
            "protect_content"
        ),
        allow_paid_broadcast: _t.Optional[bool] = None,
        message_effect_id: _t.Optional[str] = None,
        reply_parameters: _t.Optional[types.ReplyParameters] = None,
        reply_markup: _t.Optional[
            _t.Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
            ]
        ] = None,
        allow_sending_without_reply: _t.Optional[bool] = None,
        disable_web_page_preview: _t.Optional[_t.Union[bool, Default]] = Default(
            "link_preview_is_disabled"
        ),
        reply_to_message_id: _t.Optional[int] = None,
        request_timeout: _t.Optional[int] = None,
        **action_kw
    ) -> types.Message:
        async with self.chat_action(**action_kw):
            return await self.__bot__.send_message(
                chat_id=self.chat_id,
                text=text,
                business_connection_id=business_connection_id,
                message_thread_id=message_thread_id,
                parse_mode=parse_mode,
                entities=entities,
                link_preview_options=link_preview_options,
                disable_notification=disable_notification,
                protect_content=protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                message_effect_id=message_effect_id,
                reply_parameters=reply_parameters,
                reply_markup=reply_markup,
                allow_sending_without_reply=allow_sending_without_reply,
                disable_web_page_preview=disable_web_page_preview,
                reply_to_message_id=reply_to_message_id,
                request_timeout=request_timeout,
            )

    async def send_photo(
        self,
        photo: _t.Union[types.InputFile, str],
        business_connection_id: _t.Optional[str] = None,
        message_thread_id: _t.Optional[int] = None,
        caption: _t.Optional[str] = None,
        parse_mode: _t.Optional[_t.Union[str, Default]] = Default("parse_mode"),
        caption_entities: _t.Optional[list[types.MessageEntity]] = None,
        show_caption_above_media: _t.Optional[_t.Union[bool, Default]] = Default(
            "show_caption_above_media"
        ),
        has_spoiler: _t.Optional[bool] = None,
        disable_notification: _t.Optional[bool] = None,
        protect_content: _t.Optional[_t.Union[bool, Default]] = Default(
            "protect_content"
        ),
        allow_paid_broadcast: _t.Optional[bool] = None,
        message_effect_id: _t.Optional[str] = None,
        reply_parameters: _t.Optional[types.ReplyParameters] = None,
        reply_markup: _t.Optional[
            _t.Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
            ]
        ] = None,
        allow_sending_without_reply: _t.Optional[bool] = None,
        reply_to_message_id: _t.Optional[int] = None,
        request_timeout: _t.Optional[int] = None,
        **action_kw
    ) -> types.Message:
        async with self.chat_action(ChatAction.UPLOAD_PHOTO, **action_kw):
            return await self.__bot__.send_photo(
                chat_id=self.chat_id,
                photo=photo,
                business_connection_id=business_connection_id,
                message_thread_id=message_thread_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                show_caption_above_media=show_caption_above_media,
                has_spoiler=has_spoiler,
                disable_notification=disable_notification,
                protect_content=protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                message_effect_id=message_effect_id,
                reply_markup=reply_markup,
                reply_parameters=reply_parameters,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_to_message_id=reply_to_message_id,
                request_timeout=request_timeout,
            )
