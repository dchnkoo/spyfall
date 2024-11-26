from spy.decorators import with_user_cache, with_play_room, create_user_or_update
from spy.routers import group_only_msg_without_state
from spy import filters as game_filters, game
from spy.commands import group

from utils.exc.assertion import Assertion

from aiogram import filters, types

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@group_only_msg_without_state.message(
    filters.Command(group.play),
    ~game_filters.GameProccessFilter(),
    game_filters.RegisteredUser(),
)
@with_user_cache
async def play(msg: types.Message, user: "TelegramUser", **_):
    settings = await user.get_settings()
    assert settings is not None

    room = game.GameRoom(
        id=msg.chat.id,
        creator=user,
        game_settings=settings,
        language_code=user.language,
    )

    async with room.manager(save_room=True):
        await room.start_game()


@group_only_msg_without_state.message(
    filters.Command(group.join),
    game_filters.GameProccessFilter(game.GameStatus.recruitment),
)
@create_user_or_update
async def joint_to_the_game(msg: types.Message, user: "TelegramUser", **_):
    room = await game.GameRoom.load_cached(msg.chat.id)
    try:
        await room.add_player(user)
    except AssertionError as e:
        handler = None
        for handler in Assertion.is_assertion(e):
            ...
        if not handler:
            raise e
    await msg.delete()


@group_only_msg_without_state.message(
    filters.Command(group.end),
    game_filters.GameProccessFilter(),
    filters.or_f(
        game_filters.PlayerFilter(is_creator=True),
        game_filters.ChatMemberIsAdmin(answer=False),
    ),
)
@with_play_room(save_after=False)
async def end_the_game(msg: types.Message, play_room: game.GameRoom, **_):
    await play_room.finish_game()


@group_only_msg_without_state.message(
    game_filters.GameProccessFilter(),
)
async def cleaner(msg: types.Message):
    await msg.delete()
