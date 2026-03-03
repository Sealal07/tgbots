import random
from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from database.engine import SessionLocal
from database.models import TestQuestion, User
from utils.keyboards import  quiz_levels
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton

router = Router()

@router.message(F.text == '📝 Тесты')
async def start_quiz(message: Message):
    await message.answer('Выбери уровень сложности для теста:',
                         reply_markup=quiz_levels())

@router.callback_query(F.data.startswith('quiz_'))
async def send_quiz_poll(callback: CallbackQuery):
    # callback_data='quiz_A1'
    level = callback.data.split('_')[1]

    async with SessionLocal() as session:
        result = await session.execute(select(TestQuestion).where(TestQuestion.level == level))
        questions = result.scalars().all()
        if not questions:
            await callback.answer('Для этого уровня еще не добавлены вопросы',
                                  show_alert=True)
            return
        q = random.choice(questions)
        options = q.options.split(',')
        await callback.message.answer_poll(
            question=q.question_text,
            options=options,
            type='quiz',
            correct_option_id=q.correct_option,
            is_anonymous=False
        )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='➡️Следующий вопрос',
                                     callback_data=f'quiz_{level}'))
    builder.row(InlineKeyboardButton(text='🛑Завершить тест',
                                     callback_data='stop_quiz'))
    await callback.message.answer('Выбери ответ и нажми "Следующий", чтобы продолжить',
                                  reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data == 'stop_quiz')
async def stop_quiz(callback: CallbackQuery):
    await callback.message.edit_text('Тестирование завершено.Возвращайся скорее!')
