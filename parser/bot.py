import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from database import init_db
import car_bot
import logging

TOKEN = '8686841919:AAH1emC4-F3BzUqu0NBXEHdc3p6I4ydB2Mc'

bot = Bot(token=TOKEN)
dp = Dispatcher()

brands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Toyota'), KeyboardButton(text='BMW')],
        [KeyboardButton(text='Audi'), KeyboardButton(text='Mercedes')],
        [KeyboardButton(text='Kia'), KeyboardButton(text='Hyundai')],
        [KeyboardButton(text='Все марки')]
    ],resize_keyboard=True
)

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer('🚗Привет! Я бот-парсер\n Выберите марку машины: ',
                         reply_markup=brands_keyboard)

@dp.message(lambda message: message.text in ['Toyota', 'BMW', 'Audi', 'Mercedes', 'Kia', 'Hyundai', 'Все марки'])
async def handle_brand_selection(message: Message):
    brand = message.text if message.text != 'Все марки' else ''
    await send_car_list(message, brand)

async def send_car_list(message: Message, brand: str):
    cars_data = car_bot.get_cars(brand)
    if cars_data:
        for car in cars_data:
            response_text = (
                f'🚖{car['title']}\n'
                f'💰Цена: {car['price']}\n'
                f'📊{car['params']}\n'
                f'🖇{car['link']}\n'
                f'{'='*30}'
            )
            await message.answer(response_text)
    else:
        await message.answer('ничего не найдено или произошла ошибка')

async def main():
    logging.basicConfig(level=logging.INFO)
    print('инициализация БД')
    init_db()
    print('бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
