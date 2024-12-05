from spy.routers import group_without_state
from spy.decorators import with_user_cache
from spy import texts

from aiogram import F, types, Bot, enums

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@group_without_state.message(F.content_type == types.ContentType.NEW_CHAT_MEMBERS)
@with_user_cache
async def added_to_group(msg: types.Message, user: "TelegramUser", bot: Bot):
    for member in msg.new_chat_members:
        if member.id == bot.id:
            await msg.answer(
                texts.GREETINGS_MSG_IN_GROUP,
                parse_mode=enums.ParseMode.MARKDOWN_V2,
            )
