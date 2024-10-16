from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='8116457190:AAH6z1ebWXcoD4s-zXk1Xk0YWVNPMKT52Io')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
kb = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb.add(button1, button2)
# kb.row(button1, button2)

# Клавиатура для повторного расчета"
repeat_kb = InlineKeyboardMarkup(resize_keyboard=True)
repeat_button1 = InlineKeyboardButton(text='Да', callback_data='calories')
repeat_button2 = InlineKeyboardButton(text='Нет', callback_data='stop')
repeat_kb.add(repeat_button1, repeat_button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer('Формула Миффлина для мужчин:\n10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')
    await call.answer()
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.callback_query_handler(text='calories')
async def cmd_start(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в см):')
    await UserState.next()

@dp.message_handler(state=UserState.growth)
async def process_growth(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в кг):')
    await UserState.next()

@dp.message_handler(state=UserState.weight)
async def process_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Формула для мужчин
    norma = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5

    await message.answer(f"Ваша суточная норма калорий составляет:\n{round(norma)} ккал")
    await state.finish()

    # Отправляем сообщение с кнопкой "Повторить расчет?"
    await message.answer("Хотите повторить расчет?", reply_markup=repeat_kb)

    # Обработчик для кнопки "Нет"
    @dp.callback_query_handler(text='stop')
    async def stop_interaction(call: types.CallbackQuery):
        await call.message.answer("Хорошо! Если понадоблюсь, просто напиши /start.")
        await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
