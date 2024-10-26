from aiogram import types, F, Router
from aiogram.filters import Command
from bot_config import database


dishes_router = Router()


@dishes_router.callback_query(lambda call: call.data == "dishes")
async def dishes_handler(call: types.CallbackQuery):
    sql = """
    SELECT * FROM dishes ORDER BY price DESC
    """
    data = database.fetch(sql)
    counter = 1
    await call.message.answer("Список блюд:")
    for dish in data:
        await call.message.answer(f"{counter}. {dish[1]}\nЦена: {dish[2]} сом\nКатегория: {dish[3]}")
        counter += 1


@dishes_router.message(Command("dishes"))
async def dishes_handler(message: types.Message):
    sql = """
    SELECT * FROM dishes ORDER BY price DESC
    """
    data = database.fetch(sql)
    counter = 1
    await message.answer("Список блюд:")
    for dish in data:
        await message.answer(f"{counter}. {dish[1]}\nЦена: {dish[2]} сом\nКатегория: {dish[3]}")
        counter += 1
