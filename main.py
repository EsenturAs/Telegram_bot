import asyncio
import logging
from aiogram import Bot


from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.random import random_router
from handlers.myinfo import myinfo_router
from handlers.review_dialog import review_router
from databases.database import Database
import sqlite3


async def on_startup(bot: Bot):
    print("Бот запустился")
    db = Database(database)
    db.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(myinfo_router)
    dp.include_router(review_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
