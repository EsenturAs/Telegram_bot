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
    await call.message.answer("Введите категорию блюда")


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
    await message.answer("Введите категорию блюда")


def category_filter(message: types.Message):
    category = message.text
    categories = database.fetch(f"SELECT * FROM dish_categories WHERE name = '{category}'")
    print(categories)
    if categories:
        return {"category": categories[0][1]}
    else:
        return False


@dishes_router.message(category_filter)
async def show_dishes_by_category(message: types.Message, category: str):
    dishes = database.fetch(f"""
    SELECT dishes.name, dishes.price, dish_categories.name AS category_name FROM dishes
    JOIN dish_categories ON dishes.category_id = dish_categories.id
    WHERE dish_categories.name = '{category}'
    """)
    if len(dishes) == 0:
        await message.answer("Ничего не найдено")
        return
    await message.answer("Блюда введенной категории:")
    print(dishes)
    counter = 1
    for dish in dishes:
        await message.answer(f"{counter}. {dish[0]}\nЦена: {dish[1]} сом\nКатегория: {dish[2]}")
        counter += 1

