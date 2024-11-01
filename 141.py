import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = 'YOUR_API_TOKEN'  # Замените на ваш токен

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация базы данных
# initiate_db()  # Комментарий, так как функция не определена в предоставленном коде

# Определение состояний пользователя
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

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)

@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)

@dp.message_handler(text='Купить')  # Обработчик для кнопки "Купить"
async def get_buying_list(message: types.Message):
    products = [
        ('Product1', 'Описание 1', 1, 'https://i.pinimg.com/736x/e5/de/94/e5de9481f54df4a712525431338c3497.jpg'),
        ('Product2', 'Описание 2', 2, 'https://images.squarespace-cdn.com/content/v1/607773ecd359161f2364e7c9/1622838803922-WEOBACY2T9I8AHFQPDGJ/vitaminC.png'),
        ('Product3', 'Описание 3', 3, 'https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_728,h_389/https://www.medicynanaroda.ru/wp-content/uploads/2017/11/v-kakix-produktax-soderzhitsya-vitamin-d.jpg'),
        ('Product4', 'Описание 4', 4, 'https://avatars.mds.yandex.net/i?id=cf694584172248a40c4d1bc3fdb4832e_l-10355200-images-thumbs&n=13'),
    ]

    for name, description, price, image_url in products:
        await message.answer(f'Название: {name} | Описание: {description} | Цена: {price * 100} рублей')
        await message.answer_photo(photo=image_url)

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)

    @dp.callback_query_handler(text='product_buying')
    async def send_confirm_message(call: types.CallbackQuery):
        await call.message.answer("Вы успешно приобрели продукт!")
        await call.answer()

    @dp.callback_query_handler(text='formulas')
    async def get_formulas(call: types.CallbackQuery):
        await call.message.answer(
            "Формула Миффлина-Сан Жеора:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
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

    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)