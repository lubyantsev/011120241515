import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA'  # Убедитесь, что вы убрали ваш токен перед загрузкой на GitHub

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token='7496069476:AAEmEJvx70OUkElm_JV8q4BypnswN3Nk0aA')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Создаем обычную клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton('Рассчитать')
button_info = KeyboardButton('Информация')
keyboard.add(button_calculate, button_info)

# Создаем Inline клавиатуру
inline_keyboard = InlineKeyboardMarkup()
button_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard.add(button_calories, button_formulas)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Формула Миффлина-Сан Жеора:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.answer('Введите свой возраст:')
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.reply('Введите свой рост:')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.reply('Введите свой вес:')

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    # Пример формулы для расчёта
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.reply(f'Ваша норма калорий: {bmr:.2f} ккал.')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)