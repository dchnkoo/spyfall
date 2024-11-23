from spy.decorators import with_user_cache
from spy.routers import private_only_msg
from spy.commands import private
from spy import fsm, texts

from aiogram import types, filters

import typing as _t

if _t.TYPE_CHECKING:
    from database import TelegramUser


@private_only_msg.message(
    filters.StateFilter("*"),
    filters.Command(private.skip),
)
@with_user_cache
async def skip(
    message: types.Message,
    state: fsm.FSMContext,
    user: "TelegramUser",
    **_,
):
    current_state = await state.get_state()

    if current_state is None:
        return

    cls_str, field_str = current_state.split(":", 1)

    cls: type[fsm.UpgradedStatesGroup] = getattr(fsm, cls_str)
    field = getattr(cls, field_str)

    index = cls.__states__.index(field)

    next_step_txt = None
    if (next_state := (index + 1)) <= len(cls.__states__) - 1:
        st: fsm.State = cls.__states__[next_state]
        state_name = st.state.split(":", 1)[1]

        if state_name == "save":
            await cls._save(message, state, user)
            await state.clear()
            return

        await state.set_state(st)

        txt = texts.SKIPED_ACTION

        new_state = st.state.split(":", 1)[1]
        data = cls.msgs.get(new_state, None)

        if data is not None:
            next_step_txt = data[0]
    else:
        await state.clear()
        txt = texts.CANCELED_ACTION

    await message.answer(txt)

    if next_step_txt is not None:
        await message.answer(next_step_txt)
