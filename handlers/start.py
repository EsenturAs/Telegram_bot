from aiogram import Router, types, F
from aiogram.filters.command import Command


start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):

    name = message.from_user.first_name
    uid = str(message.from_user.id)
    with open("ids.txt", "r") as read_file:
        ids = read_file.readline().split()
        if uid not in ids:
            with open("ids.txt", "a") as a_file:
                a_file.write(f" {uid}")
            count = len(ids) + 1
        elif uid in ids:
            count = len(ids)

        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="Наш адрес", callback_data="address"),
                    types.InlineKeyboardButton(text="Контакты", callback_data="contacts")
                ],
                [
                    types.InlineKeyboardButton(text="О нас", callback_data="aboutus"),
                    types.InlineKeyboardButton(text="Наш сайт", url="https://navat.kg")
                ]
            ]
        )

        await message.answer(f"Привет, {name}, наш бот обслуживает уже {count} пользователя.")


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


