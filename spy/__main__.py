from spy.commands import group, private
from spy.routers import spybot
from spy.points import dp

from base_package.base_package import upload_base_locations

from aiogram.methods import DeleteWebhook
from aiogram import types

from loguru import logger

import asyncio


async def main():
    await upload_base_locations()
    await spybot(DeleteWebhook(drop_pending_updates=True))

    await spybot.set_my_commands(list(private), types.BotCommandScopeAllPrivateChats())
    await spybot.set_my_commands(
        list(group),
        types.BotCommandScopeAllGroupChats(),
    )

    logger.info("Bot start working..")
    await dp.start_polling(spybot)


if __name__ == "__main__":
    asyncio.run(main())
