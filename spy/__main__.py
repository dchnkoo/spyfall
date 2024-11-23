from spy.routers import spybot
from spy.points import dp

from aiogram.methods import DeleteWebhook

import asyncio


async def main():
    await spybot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(spybot)


if __name__ == "__main__":
    asyncio.run(main())
