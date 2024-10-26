from aiogram import Router, types, F
from aiogram.filters.command import Command
from bot_config import database


start_router = Router()


def add_user(message: types.Message):
    name = message.from_user.first_name
    tg_id = str(message.from_user.id)
    sql = f"""
    SELECT tg_id FROM users WHERE tg_id = '{tg_id}'
    """
    user = database.fetch(sql)
    if len(user) == 0:
        sql = f"""
            INSERT INTO users (name, tg_id) VALUES (
            '{name}',
            {tg_id}
            )
            """
        database.execution(sql)
    else:
        pass



@start_router.message(Command("start"))
async def start_handler(message: types.Message):

    name = message.from_user.first_name
    add_user(message)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Посмотреть блюда", callback_data="dishes")
            ],
            [
                types.InlineKeyboardButton(text="Наш адрес", callback_data="address"),
                types.InlineKeyboardButton(text="Контакты", callback_data="contacts")
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="aboutus"),
                types.InlineKeyboardButton(text="Наш сайт", url="https://navat.kg")
            ],
            [
                types.InlineKeyboardButton(text="Вакансии", callback_data="vacancies"),
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review")
            ],
            [
                types.InlineKeyboardButton(text="Добавить блюдо", callback_data="adddish"),
                types.InlineKeyboardButton(text="Добавить категорию", callback_data="addcategory")
            ]
        ]
    )

    await message.answer(f"Здравствуйте, {name}, Вас приветствует бот чайханы 'Нават!' "
                         f"Наш бот обслуживает уже {len(database.fetch("SELECT tg_id FROM users"))} пользователя(ей).",
                         reply_markup=kb)


@start_router.callback_query(F.data == "address")
async def about_us_handler(callback: types.CallbackQuery):
    text = "Адреса:\nул. Ибраимова 42\nул. Киевская 114/1"
    await callback.message.answer(text)


@start_router.callback_query(F.data == "contacts")
async def about_us_handler(callback: types.CallbackQuery):
    text = "Контакты:\n+996 (551) 57 11 11\n+996 (551) 53 11 11"
    await callback.message.answer(text)


@start_router.callback_query(F.data == "aboutus")
async def about_us_handler(callback: types.CallbackQuery):
    text = ("Чайхана NAVAT — это результат слияния почитание восточной культуры и современных традиций. "
            "История его создания началась, когда основатели осознали недостаток аутентичных восточных ресторанов, "
            "где можно было бы полностью погрузиться в атмосферу этно вайба и насладиться особенными вкусами "
            "восточной кухни.")
    await callback.message.answer(text)


@start_router.callback_query(F.data == "vacancies")
async def about_us_handler(callback: types.CallbackQuery):
    text = "Вакансии:\n1)Администратор\n2)Официант\n3)Повар\n4)Бармен"
    await callback.message.answer(text)
