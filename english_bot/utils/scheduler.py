import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from sqlalchemy import select, func
from database.engine import SessionLocal
from database.models import User, Word
from sqlalchemy.testing.suite.test_reflection import users


async def send_daily_word(bot: Bot):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Word).order_by(func.random()).limit(1)
        )
        word_data = result.scalar_one_or_none()
        user_result = await session.execute(select(User.id))
        user_ids = user_result.scalars().all()
        text = (
            f'**Слово дня: {word_data.word}**\n'
            f'Перевод: {word_data.translate}\n'
            f'Пример: _{word_data.example}_'
        )
        for user_id in user_ids:
            try:
                await bot.send_message(user_id, text, parse_mode='Markdown')
            except Exception as e:
                logging.error(f'Ошибка при отправке пользователю {user_id}: {e}')

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_word,
        'cron',
        hour=10,
        minute=0,
        args=[bot],
        timezone='Asia/Novosibirsk'
    )
    return scheduler