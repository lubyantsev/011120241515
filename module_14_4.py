from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Initialize the bot and dispatcher
bot = Bot(token='')  # Replace with your actual token
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define user states for FSM
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Handler for the "Купить" button
@dp.message_handler(text='Купить')  # Обработчик для кнопки "Купить"
async def get_buying_list(message: types.Message):
    products = [
        ('Product1', 'Описание 1', 1, 'https://i.pinimg.com/736x/e5/de/94/e5de9481f54df4a712525431338c3497.jpg'),
        ('Product2', 'Описание 2', 2, 'https://images.squarespace-cdn.com/content/v1/607773ecd359161f2364e7c9/1622838803922-WEOBACY2T9I8AHFQPDGJ/vitaminC.png'),
        ('Product3', 'Описание 3', 3, 'https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_728,h_389/https://www.medicynanaroda.ru/wp-content/uploads/2017/11/v-kakix-produktax-soderzhitsya-vitamin-d.jpg'),
        ('Product4', 'Описание 4', 4, 'https://avatars.mds.yandex.net/i?id=cf694584172248a40c4d1bc3fdb4832e_l-10355200-images-thumbs&n=13'),
    ]

    for name, description, price, image_url in products:
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text=f'Купить {name}', callback_data='product_buying'))

        # Отправка сообщения с фотографией и описанием продукта
        await message.answer_photo(photo=image_url, caption=f"{name}\n{description}\nЦена: {price} рублей", reply_markup=inline_keyboard)

# Handler for product buying confirmation
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

# Handler for displaying formula
@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Формула Миффлина-Сан Жеора:\nBMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
    await call.answer()

# Handler for starting the calorie input process
@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await UserState.age.set()
    await call.message.answer('Введите свой возраст:')
    await call.answer()

# FSM handler for age input
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.reply('Введите свой рост:')

# FSM handler for growth input
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.reply('Введите свой вес:')

# FSM handler for weight input and finishing the process
@dp.message_handler(state=UserState.weight)
async def finish_input(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = data.get('age')
    growth = data.get('growth')
    weight = data.get('weight')
    await message.reply(f'Ваш возраст: {age}, рост: {growth}, вес: {weight}')
    await state.finish()

# Start polling
if __name__ == '__main__':  # Corrected this line
    executor.start_polling(dp, skip_updates=True)