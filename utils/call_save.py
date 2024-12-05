from aiogram import types, Router, F, filters

from spy.decorators import with_user_cache
from spy.commands import private
from spy import fsm

import typing as _t


def call_save(
    router: Router,
    *f,
    call_after: _t.Callable[[types.Message | types.CallbackQuery], _t.Coroutine] = None,
):
    @router.message(
        *f,
        filters.or_f(
            filters.Command(private.skip, ignore_case=True),
            ~F.text.startswith("/"),
        ),
    )
    @with_user_cache
    async def save(message: types.Message, state: fsm.FSMContext, **_):
        s = await state.get_state()
        cls_str, field = s.split(":", 1)

        if not (text := message.text).startswith("/"):
            await state.update_data({field: text})

        cls = getattr(fsm, cls_str)
        msg = await cls._save(message, state, **_)

        if call_after is not None and msg is not None:
            await call_after(msg)

    def decorator(func):
        return func

    return decorator
