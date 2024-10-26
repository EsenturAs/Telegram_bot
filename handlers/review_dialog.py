from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from bot_config import database


review_router = Router()


# def has_written_review(call: types.CallbackQuery):
#     uid = str(call.from_user.id)
#     with open("reviews.txt", "r") as read_file:
#         ids = read_file.readline().split()
#         if uid not in ids:
#             toggle = False
#         elif uid in ids:
#             toggle = True
#     return toggle


def has_written_review(call: types.CallbackQuery):      # using database
    uid = str(call.from_user.id)
    sql = f"""SELECT tg_id FROM review_results WHERE tg_id = {uid}"""
    if len(database.fetch(sql)) > 0:
        return True
    else:
        return False


class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    confirmation = State()


@review_router.callback_query(lambda call: call.data == "review")
async def review_handler(call: types.CallbackQuery, state: FSMContext):
    if has_written_review(call):
        await call.message.answer("Вы уже оставили отзыв")
    else:
        await state.set_state(RestaurantReview.name)
        await call.message.answer("Как Вас зовут?")


@review_router.message(Command("stop"))
@review_router.message(F.text == "стоп")
async def stop_review_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Остановлено")


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer("Ваш номер телефона?")


@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
        await message.answer("Вводите только цифры")
        return
    await state.update_data(phone_number=phone_number)
    await state.set_state(RestaurantReview.food_rating)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Как Вы оцениваете наши блюда?", reply_markup=kb)


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    food_rating = message.text
    if not food_rating.isdigit() or (int(food_rating) < 1 or int(food_rating) > 5):
        await message.answer("Вводите только цифры от 1 до 5")
        return
    await state.update_data(food_rating=food_rating)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Как Вы оцениваете чистоту наших ресторанов?")


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    cleanliness_rating = message.text
    if not cleanliness_rating.isdigit()  or (int(cleanliness_rating) < 1 or int(cleanliness_rating) > 5):
        await message.answer("Вводите только цифры от 1 до 5")
        return
    kb = types.ReplyKeyboardRemove()
    await state.update_data(cleanliness_rating=cleanliness_rating)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Пожалуйста напишите комментарии или жалобы", reply_markup=kb)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
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
    await state.set_state(RestaurantReview.confirmation)
    await message.answer("Сохранить данные?", reply_markup=kb)


@review_router.message(RestaurantReview.confirmation, F.text == "Да")
async def process_confirmation_yes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sql = f"""
            INSERT INTO review_results (name, phone_number, food_rating, cleanliness_rating, extra_comments, tg_id) VALUES 
            ('{data["name"]}', 
            '{data["phone_number"]}', 
            '{data["food_rating"]}', 
            '{data["cleanliness_rating"]}', 
            '{data["extra_comments"]}', 
            '{message.from_user.id}'
            )
            """
    database.execution(sql)
    kb = types.ReplyKeyboardRemove()
    database.execution(sql)
    await message.answer("Спасибо за пройденный отпрос", reply_markup=kb)
    await state.clear()


@review_router.message(RestaurantReview.confirmation, F.text == "Нет")
async def process_confirmaton_no(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.set_state(RestaurantReview.name)
    await message.answer("Как Вас зовут?", reply_markup=kb)
