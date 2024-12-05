from spy.decorators import create_user_or_update, decode_start_link
from spy.routers import private_only_msg_without_state
from spy.callback import CallbackPrefix
from spy.commands import private
from spy import texts, game

from database import Settings

from aiogram.utils.deep_linking import create_startgroup_link, decode_payload
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types, filters, Bot, F

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg_without_state.message(
    filters.Command(private.start, magic=F.args.is_(None))
)
@create_user_or_update
async def start_command(msg: types.Message, bot: Bot, user: "TelegramUser", **_):
    link = await create_startgroup_link(bot, "true")

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.ADD_ME_TO_GROUP,
            url=link,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.SHOW_PACKAGES,
            callback_data=CallbackPrefix.show_packages,
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text=texts.GAME_SETTINGS,
            callback_data=CallbackPrefix.game_settings,
        )
    )
    keyboard.adjust(1, 2)

    await user.send_message(
        texts.START_MSG.format(user=user),
        reply_markup=keyboard.as_markup(),
    )


@private_only_msg_without_state.message(
    filters.Command(
        private.start,
        magic=F.args.func(
            lambda args: decode_payload(args).startswith(game.GameRoom.prefix)
        ),
    ),
)
@create_user_or_update
@decode_start_link
async def join_to_the_game(
    message: types.Message, playload: str, user: "TelegramUser", **_
):
    manager = game.GameManager.meta.get_room(
        int(playload.removeprefix(game.GameRoom.prefix))
    )

    if manager is None:
        await user.send_message(texts.ROOM_NOT_FOUND)
        return

    try:
        await manager.room.add_player(user)
    except game.exc.GameException as e:
        raise game.exc.GameExceptionWrapper(manager, e)
