import asyncio
from aiogram import types, Bot, Dispatcher
from dotenv import dotenv_values
import logging


from handlers.start import start_router
from handlers.random import random_router
from handlers.myinfo import myinfo_router


token = dotenv_values('.env')['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(myinfo_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

