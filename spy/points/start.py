from spy.routers import private_only_msg_without_state
from spy.decorators import create_user_or_update
from spy.callback import CallbackPrefix
from spy.commands import private
from spy import texts

from database import Settings

from aiogram.utils.deep_linking import create_startgroup_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, filters, Bot

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg_without_state.message(filters.Command(private.start))
@create_user_or_update
async def start_command(msg: types.Message, bot: Bot, user: "TelegramUser", **_):
    if not (await user.get_settings()):
        await Settings.add({"user_id": user.id})

    link = await create_startgroup_link(bot, "true")

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.ADD_ME_TO_GROUP(user.language),
            url=link,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.SHOW_PACKAGES(user.language),
            callback_data=CallbackPrefix.show_packages,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=await texts.GAME_SETTINGS(user.language),
            callback_data=CallbackPrefix.game_settings,
        )
    )
    keyboard.adjust(1, 2)

    await bot.set_my_commands(list(private), language_code=user.language)
    await user.send_message(
        (await texts.START_MSG(user.language)).format(user=user),
        reply_markup=keyboard.as_markup(),
    )
