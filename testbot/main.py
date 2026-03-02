# import aiogram
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command


TOKEN = '8686841919:AAH1emC4-F3BzUqu0NBXEHdc3p6I4ydB2Mc'

bot =Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer('Привет! пришли мне текст, фото или аудио')


@dp.message(F.text)
async def text_handler(message: types.Message):
    await message.reply(f'Ты написал {message.text}')

@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await message.reply('Хорошее фото')

@dp.message(F.audio | F.voice)
async def audio_handler(message: types.Message):
    await message.reply('я слышу звук')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')






# Bot - интерфейс взаимодействия с ТГ
# Dispatcher - мозг, принимает обновления от ТГ
# Router - маршруты
# Types - классы объектов ТГ (кнопки, сообщения, чат, пользователь...)
# F - фильтр F.text == 'Привет!'