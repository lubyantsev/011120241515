import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

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


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Напишите 'Calories', чтобы начать.")


@dp.message_handler(text='Calories')
async def set_age(message: types.Message):
    await UserState.age.set()
    await message.reply('Введите свой возраст:')


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
    # Для женщин: BMR = 10*weight + 6.25*growth - 5*age - 161
    # Для мужчин: BMR = 10*weight + 6.25*growth - 5*age + 5
    # Здесь я выбрал формулу для женщин, вы можете изменить по необходимости
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.reply(f'Ваша норма калорий: {bmr:.2f} ккал.')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)