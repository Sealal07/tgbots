from aiogram import Router, types
from aiogram.filters import CommandStart
from database.engine import get_or_create_user
from utils.keyboards import main_menu
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        'Welcome! Я твой English Learning Companion. Выберите действие в меню ниже:',
        reply_markup=main_menu()
    )