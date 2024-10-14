import subprocess

from aiogram import Router, types, F
from aiogram.filters.command import Command
import handlers.review_dialog


start_router = Router()


def user_counter(uid):
    with open("ids.txt", "r") as read_file:
        ids = read_file.readline().split()
        if uid not in ids:
            with open("ids.txt", "a") as a_file:
                a_file.write(f" {uid}")
            count = len(ids) + 1
        elif uid in ids:
            count = len(ids)
        print(count)
        return count


@start_router.message(Command("start"))
async def start_handler(message: types.Message):

    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш адрес", callback_data="address"),
                types.InlineKeyboardButton(text="Контакты", callback_data="contacts")
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="aboutus"),
                types.InlineKeyboardButton(text="Наш сайт", url="https://navat.kg")
            ],
            [
                types.InlineKeyboardButton(text="Вакансии", callback_data="vacancies")
            ],
            [
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review")
            ]
        ]
    )

    await message.answer(f"Здравствуйте, {name}, Вас приветствует бот чайханы 'Нават!' "
                         f"Наш бот обслуживает уже {user_counter(str(message.from_user.id))} пользователя.", reply_markup=kb)


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


@start_router.callback_query(F.data == "review")
async def start_review_handler(callback: types.CallbackQuery):
    await callback.message.answer("/review")
