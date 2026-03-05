from database.models import Idiom
from database.engine import SessionLocal
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, func

router = Router()

@router.message(F.text == '💡 Идиома дня')
async def idiom_handler(message: Message):
    async with SessionLocal() as session:
        result = await session.execute(select(Idiom).order_by(func.random()).limit(1))
        idiom_data = result.scalar_one_or_none()
        text = (
            f"💡 **Идиома:** {idiom_data.phrase}\n"
            f"✅ **Перевод:** {idiom_data.translate}\n"
            f"📝 **Пример:** {idiom_data.example}\n"
                )
        await message.answer(text, parse_mode='Markdown')