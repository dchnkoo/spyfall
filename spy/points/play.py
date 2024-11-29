from spy.decorators import with_user_cache, with_manager, create_user_or_update
from spy.game import GameManager, GameStatus, GameRoom
from spy.routers import group_only_msg_without_state
from spy import filters as game_filters
from spy.commands import group

from aiogram import filters, types

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@group_only_msg_without_state.message(
    filters.Command(group.play),
    ~game_filters.GameProccessFilter(),
    ~game_filters.PlayerFilter(),
    game_filters.RegisteredUser(),
)
@with_user_cache
async def play(msg: types.Message, user: "TelegramUser", **_):
    settings = await user.get_settings()
    assert settings is not None

    room = GameRoom(
        id=msg.chat.id,
        creator=user,
        game_settings=settings,
        language_code=user.language,
    )

    manager = await GameManager.register(room=room)
    await manager.queue.put(GameStatus.recruitment)


@group_only_msg_without_state.message(
    filters.Command(group.start_playing),
    game_filters.GameProccessFilter(GameStatus.recruitment),
    game_filters.PlayerFilter(is_creator=True),
)
@with_manager
async def start_playing(msg: types.Message, manager: GameManager, **_):
    manager.cancel_current_task()
    await manager.room.delete_sended_messages()
    await manager.queue.put(GameStatus.playing)


@group_only_msg_without_state.message(
    filters.Command(group.join),
    game_filters.GameProccessFilter(GameStatus.recruitment),
)
@create_user_or_update
@with_manager
async def joint_to_the_game(
    msg: types.Message, user: "TelegramUser", manager: GameManager, **_
):
    try:
        await manager.room.add_player(user)
    finally:
        await msg.delete()


@group_only_msg_without_state.message(
    filters.Command(group.end),
    game_filters.GameProccessFilter(),
    filters.or_f(
        game_filters.PlayerFilter(is_creator=True),
        game_filters.ChatMemberIsAdmin(answer=False),
    ),
)
@with_manager
async def end_the_game(msg: types.Message, manager: GameManager, **_):
    await manager.finish_game()


@group_only_msg_without_state.message(
    game_filters.GameProccessFilter(),
)
async def cleaner(msg: types.Message):
    await msg.delete()
