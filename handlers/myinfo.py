from aiogram import Router, types
from aiogram.filters.command import Command


myinfo_router = Router()


@myinfo_router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    info = f"Ващ id: {message.from_user.id}, Ваш имя:{message.from_user.first_name} Ваш юзернейм: {message.from_user.username}"
    await message.answer(info)