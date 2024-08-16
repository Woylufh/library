from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *
from crud_functions import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Рассчитать')

        ], [KeyboardButton(text='Регистрация')]

    ], resize_keyboard=True
)

kb_lin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]
    ]
)

kb_lin2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)



@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит): ")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    username = await state.get_data()
    user = username['username']
    if is_included(user) is True:
        await message.answer('Пользователь уже существует, введите другое имя')
        await RegistrationState.username.set()
    else:
        await message.answer(f'Ваше имя{username}.\nВведите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    email = await state.get_data()
    await message.answer(f'Ваша почта {email}.\n"Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer(f'ваш возраст {data}.')
    user = data['username']
    mail = data['email']
    age = data['age']
    add_user(user, mail, age)
    await message.answer('Регистрация прошла успешно!')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('301.png', 'rb') as img1:
        await message.answer_photo(img1, get_all_products(1))
    with open('302.png', 'rb') as img2:
        await message.answer_photo(img2, get_all_products(2))
    with open('303.png', 'rb') as img3:
        await message.answer_photo(img3, get_all_products(3))
    with open('304.png', 'rb') as img4:
        await message.answer_photo(img4, get_all_products(4))
        await message.answer("Выберите продукт для покупки:", reply_markup=kb_lin)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()
    pass


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_lin2)


form = ('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    age = await state.get_data()
    await message.answer(f'ваш возраст {age}.\nВведите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    growth = await state.get_data()
    await message.answer(f'Ваш рост {growth}.\nВведите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = 10 * int(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваш вес {data}.Ваша суточная норма ккал. {a}')
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)