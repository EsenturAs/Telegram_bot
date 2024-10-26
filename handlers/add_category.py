from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from bot_config import database, admin_id


add_category_router = Router()


class NewCategory(StatesGroup):
    name = State()
    confirmation = State()


@add_category_router.callback_query(lambda call: call.data == "addcategory")
async def start_add_category(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != admin_id:
        await call.message.answer("Доступ запрещен")
        print(call.from_user.id, admin_id)
    else:
        await state.set_state(NewCategory.name)
        await call.message.answer("Название новой категории:")


@add_category_router.message(Command("stop"))
@add_category_router.message(F.text == "стоп")
async def stop_add_dish_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Остановлено")


@add_category_router.message(NewCategory.name)
async def process_name(message: types.Message, state: FSMContext):
    sql = """
    SELECT name FROM dish_categories
    """
    categories = database.fetch(sql)
    if message.text in categories:
        print("Такая категория уже есть")
        return
    else:
        await state.update_data(name=message.text)
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="Да"),
                    types.KeyboardButton(text="Нет")
                ]
            ],
            resize_keyboard=True
        )
        await message.answer("Сохранить данные?", reply_markup=kb)
        await state.set_state(NewCategory.confirmation)


@add_category_router.message(NewCategory.confirmation, F.text == "Да")
async def process_confirmation_yes(message: types.Message, state: FSMContext):
    await state.update_data()
    data = await state.get_data()
    kb = types.ReplyKeyboardRemove()
    await message.answer("Данные сохранены", reply_markup=kb)
    sql = f"""
    INSERT INTO dish_categories (name) VALUES ('{data["name"]}')
    """
    database.execution(sql)


@add_category_router.message(NewCategory.confirmation, F.text == "Нет")
async def process_confirmaton_no(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.set_state(NewCategory.name)
    await message.answer("Название нового категории", reply_markup=kb)