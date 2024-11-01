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
button_buy = KeyboardButton('Купить')  # Кнопка "Купить"
keyboard.add(button_calculate, button_info, button_buy)

# Создаем Inline клавиатуру
inline_keyboard = InlineKeyboardMarkup()
button_product1 = InlineKeyboardButton('Product1', callback_data='product_buying')
button_product2 = InlineKeyboardButton('Product2', callback_data='product_buying')
button_product3 = InlineKeyboardButton('Product3', callback_data='product_buying')
button_product4 = InlineKeyboardButton('Product4', callback_data='product_buying')
inline_keyboard.add(button_product1, button_product2, button_product3, button_product4)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)

@dp.message_handler(text='Купить')  # Обработчик для кнопки "Купить"
async def get_buying_list(message: types.Message):
    products = [
        ('Product1', 'Описание 1', 1),
        ('Product2', 'Описание 2', 2),
        ('Product3', 'Описание 3', 3),
        ('Product4', 'Описание 4', 4)
    ]

    for name, description, price in products:
        await message.answer(f'Название: {name} | Описание: {description} | Цена: {price * 100}')
        await message.answer_photo(photo='https://i.pinimg.com/736x/e5/de/94/e5de9481f54df4a712525431338c3497.jpg')
        await message.answer_photo(photo='https://images.squarespace-cdn.com/content/v1/607773ecd359161f2364e7c9/1622838803922-WEOBACY2T9I8AHFQPDGJ/vitaminC.png')
        await message.answer_photo(photo='https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_728,h_389/https://www.medicynanaroda.ru/wp-content/uploads/2017/11/v-kakix-produktax-soderzhitsya-vitamin-d.jpg')
        await message.answer_photo(photo='https://avatars.mds.yandex.net/i?id=cf694584172248a40c4d1bc3fdb4832e_l-10355200-images-thumbs&n=13')

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

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
    await message.reply('Введите свой рост (в см):')

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.reply('Введите свой вес (в кг):')

@dp.message_handler(state=UserState.weight)
async def calculate_bmr(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data.get('age'))
    growth = float(data.get('growth'))
    weight = float(data.get('weight'))

    # Пример расчета BMR по формуле Миффлина-Сан Жеора для женщин
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.reply(f"Ваш BMR: {bmr:.2f} ккал.")
    await state.finish()  # Завершить состояние

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)