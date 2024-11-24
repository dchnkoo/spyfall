from spy.commands import private
from spy import texts

from aiogram import types, filters, Router


def no_skip(router: Router, *f):

    @router.message(filters.Command(private.skip), *f)
    async def handle_no_skip(message: types.Message, **_):
        await message.answer(
            await texts.YOU_CANNOT_SKIP_THAT_ACTION(
                message.from_user.language_code or "en"
            )
        )
        return

    return handle_no_skip


def freeze_action(router: Router, *f):
    @router.message(
        filters.or_f(filters.Command(private.skip), filters.Command(private.cancel)), *f
    )
    async def wrapper(message: types.Message, **_):
        await message.answer(
            await texts.YOU_CANNOT_SKIP_THAT_ACTION(
                message.from_user.language_code or "en"
            )
        )
        return

    return wrapper
