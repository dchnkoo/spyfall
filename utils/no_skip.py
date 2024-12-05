from spy.commands import private
from spy import texts

from aiogram import types, filters, Router, enums


def no_skip(router: Router, *f):

    @router.message(filters.Command(private.skip), *f)
    async def handle_no_skip(message: types.Message, **_):
        await message.answer(
            texts.YOU_CANNOT_SKIP_THAT_ACTION,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )
        return

    return handle_no_skip


def freeze_action(router: Router, *f):
    @router.message(
        filters.or_f(filters.Command(private.skip), filters.Command(private.cancel)), *f
    )
    async def wrapper(message: types.Message, **_):
        await message.answer(
            texts.YOU_CANNOT_SKIP_THAT_ACTION,
            parse_mode=enums.ParseMode.MARKDOWN_V2,
        )
        return

    return wrapper
