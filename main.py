import asyncio
import logging


from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.random import random_router
from handlers.myinfo import myinfo_router
from handlers.review_dialog import review_router
from handlers.add_dish_dialog import add_dish_router
from handlers.dishes import dishes_router
from handlers.add_category import add_category_router


async def on_startup():
    print("Бот запустился")
    database.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(myinfo_router)
    dp.include_router(review_router)
    dp.include_router(add_dish_router)
    dp.include_router(dishes_router)
    dp.include_router(add_category_router)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
