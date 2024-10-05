from aiogram import Router, types
from aiogram.filters.command import Command
from random import choice


random_router = Router()


@random_router.message(Command("random"))
async def random_handler(message: types.Message):
    names = ("John", "Jill", "Leon", "Clair", "Chris", "Tom", "Sarah")
    await message.answer(f"Случайное имя из списка: {choice(names)}")