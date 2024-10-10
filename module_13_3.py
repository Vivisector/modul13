from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = 'KEY'
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(text=['Urban', 'ff'])
async def urban_message(message):
    await message.answer('urban message')

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Рад вас видеть!')

# @dp.message_handler(commands=['start'])
# async def start_message(message):
#     print('Start message')


@dp.message_handler()
async def all_message(message):
    await message.answer("Не понимаю(( Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)