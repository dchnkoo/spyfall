from spy.callback import CallbackPrefix
from spy.routers import dp

from aiogram import F, types


@dp.callback_query(F.data == CallbackPrefix.delete_msg)
async def delete_msg(msg: types.CallbackQuery):
    await msg.message.delete()
