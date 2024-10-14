from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


review_router = Router()


def has_written_review(message: types.Message):
    uid = str(message.from_user.id)
    with open("reviews.txt", "r") as read_file:
        ids = read_file.readline().split()
        if uid not in ids:
            toggle = False
        elif uid in ids:
            toggle = True
    return toggle


class RestaurantReview(StatesGroup):
    review_started = State()
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


@review_router.callback_query(F.data == "review")
@review_router.message(Command("review"))
async def review_handler(message: types.Message, state: FSMContext):
    if has_written_review(message):
        await message.answer("Вы уже оставили отзыв")
    else:
        await state.set_state(RestaurantReview.name)
        await message.answer("Как Вас зовут?")


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
    await state.update_data(phone_number=message.text)
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
    await message.answer("Какого Вы пола?", reply_markup=kb)
    await message.answer("Как Вы оцениваете наши блюда?")


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Как Вы оцениваете чистоту наших ресторанов?")


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    kb = types.ReplyKeyboardRemove()
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Пожалуйста напишите комментарии или жалобы", reply_markup=kb)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await state.clear()
    with open("reviews.txt", "a") as a_file:
        a_file.write(f" {str(message.from_user.id)}")
    await message.answer("Спасибо за пройденный отпрос")
