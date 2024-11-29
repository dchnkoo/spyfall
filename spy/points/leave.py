from spy.decorators import with_user_cache, with_manager
from spy.routers import private_only_msg_without_state
from spy import filters as game_filters
from spy.commands import private
from spy.game import exc

from aiogram import types, filters

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser
    from spy.game import GameManager


@private_only_msg_without_state.message(
    filters.Command(private.leave),
    game_filters.GameProccessFilter(by_user_id=True),
    ~game_filters.PlayerFilter("left"),
)
@with_user_cache
@with_manager(by_user_id=True)
async def left_the_room(
    msg: types.Message, manager: "GameManager", user: "TelegramUser", **_
):
    try:
        player = manager.room.players.get(user.id)
        assert player is not None, "Player is None"
        await manager.room.quit(player)
    except exc.GameException as e:
        raise exc.GameExceptionWrapper(manager, e)
