from spy.routers import private_only_msg
from spy.commands import private
from spy import fsm, texts

from spy.decorators import with_user_cache

from aiogram import types, filters

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg.message(
    filters.Command(private.cancel),
    filters.StateFilter("*"),
)
@with_user_cache
async def cancel(msg: types.Message, user: "TelegramUser", state: fsm.FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await user.send_message(texts.CANCELED)


@private_only_msg.message(
    filters.StateFilter("*"),
)
async def if_not_cacnel(msg: types.Message):
    await msg.delete()
