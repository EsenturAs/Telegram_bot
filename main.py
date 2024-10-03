import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import logging
from random import choice


token = dotenv_values('.env')['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    uid = str(message.from_user.id)
    # count = 0
    with open("ids.txt", "r") as read_file:
        ids = read_file.readline().split()
        if uid not in ids:
            with open("ids.txt", "a") as a_file:
                a_file.write(f" {uid}")
            count = len(ids) + 1
        elif uid in ids:
            count = len(ids)
        await message.answer(f"Привет, {name}, наш бот обслуживает уже {count} пользователя.")


@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    info = f"Ващ id: {message.from_user.id}, Ваш имя:{message.from_user.first_name} Ваш юзернейм: {message.from_user.username}"
    await message.answer(info)

@dp.message(Command("random"))
async def random(message: types.Message):
    names = ("John", "Jill", "Leon", "Clair", "Chris", "Tom", "Sarah")
    await message.answer(f"Случайное имя из списка: {choice(names)}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

