from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters import Command
from bot_config import database, admin_id


add_dish_router = Router()


class NewDish(StatesGroup):
    name = State()
    price = State()
    category = State()
    confirmation = State()


@add_dish_router.message(Command("adddish"))
async def start_add_dish_dialog(message: types.Message, state: FSMContext):
    if message.from_user.id != admin_id:
        await message.answer("Доступ запрещен")
    else:
        await state.set_state(NewDish.name)
        await message.answer("Название нового блюда")


@add_dish_router.callback_query(lambda call: call.data == "adddish")
async def start_add_dish_dialog(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != admin_id:
        await callback.answer("Доступ запрещен")
    else:
        await state.set_state(NewDish.name)
        await callback.message.answer("Название нового блюда")


@add_dish_router.message(Command("stop"))
@add_dish_router.message(F.text == "стоп")
async def stop_add_dish_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Остановлено")


@add_dish_router.message(NewDish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewDish.price)
    await message.answer("Цена нового блюда")


@add_dish_router.message(NewDish.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Вводите только цифры")
        return
    await state.update_data(price=price)
    await state.set_state(NewDish.category)
    await message.answer("Категория нового блюда")


@add_dish_router.message(NewDish.category)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Да"),
                types.KeyboardButton(text="Нет")
             ]
        ],
        resize_keyboard=True
    )

    data = await state.get_data()
    print(data)
    await state.set_state(NewDish.confirmation)
    await message.answer(f"Название: {data["name"]}\nЦена: {data["price"]}\nКатегория: {data["category"]}")
    await message.answer("Сохранить данные?", reply_markup=kb)


@add_dish_router.message(NewDish.confirmation, F.text == "Да")
async def process_confirmation_yes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # await state.update_data(confirm=NewDish.confirmation)
    sql = f"""
        INSERT INTO dishes (name, price, category) VALUES (
        '{data["name"]}',
        '{data["price"]}',
        '{data["category"]}'
        )
    """
    kb = types.ReplyKeyboardRemove()
    database.execution(sql)
    await message.answer("Данные сохранены", reply_markup=kb)
    await state.clear()


@add_dish_router.message(NewDish.confirmation, F.text == "Нет")
async def process_confirmaton_no(message: types.Message, state: FSMContext):
    await state.clear()
    kb = types.ReplyKeyboardRemove()
    await message.answer("Данные не сохранены", reply_markup=kb)
