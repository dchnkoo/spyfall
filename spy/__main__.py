from spy.commands import group, private
from spy.routers import spybot
from spy.points import dp

from aiogram.methods import DeleteWebhook
from aiogram import types

import asyncio


async def main():
    await spybot(DeleteWebhook(drop_pending_updates=True))

    await spybot.set_my_commands(list(private), types.BotCommandScopeAllPrivateChats())
    await spybot.set_my_commands(
        list(group),
        types.BotCommandScopeAllGroupChats(),
    )

    await dp.start_polling(spybot)


if __name__ == "__main__":
    asyncio.run(main())
