from aiogram import types


async def msg_answer(msg: types.Message | types.CallbackQuery, *msg_args, **msg_kw):
    is_callback = isinstance(msg, types.CallbackQuery)
    if is_callback:
        return await msg.message.answer(*msg_args, *msg_kw)
    else:
        return await msg.answer(*msg_args, *msg_kw)
