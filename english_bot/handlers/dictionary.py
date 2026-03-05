import random
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from  sqlalchemy import select
from database.engine import SessionLocal
from database.models import PersonalWord

router = Router()

@router.message(F.text == '📚 Мой словарь')
async def dictionary_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='📜 Список слов', callback_data='dict_list_0'))
    builder.row(InlineKeyboardButton(text='🧠 Карточки', callback_data='dict_cards'))
    await message.answer('Чем хочешь заняться сегодня?',reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith(f'dict_list_'))
async def show_dict_list(callback: CallbackQuery):
    page = int(callback.data.split('_')[2])
    async with SessionLocal() as session:
        result = await session.execute(
            select(PersonalWord).where(PersonalWord.user_id == callback.from_user.id).limit(10).offset(page*10)
        )
        words = result.scalars().all()
        if not words and page == 0:
            await callback.answer('В твоем словаре еще нет слов!', show_alert=True)
            return
        elif not words:
            await callback.answer('Это последняя страница!')
            return
        text = '📖 **Твои слова:**\n\n'
        for w in words:
            status = '✅' if w.is_learned else '⏳'
            text += f'{status} {w.word} - {w.translation}\n\n'
        builder = InlineKeyboardBuilder()
        if page > 0:
            builder.add(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'dict_list_{page-1}'))
        builder.add(InlineKeyboardButton(text='➡️ Вперед', callback_data=f'dict_list_{page + 1}'))

        await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode='Markdown')

@router.callback_query(F.data == 'dict_cards')
async def show_dict_cards(callback:CallbackQuery):
    async with SessionLocal() as session:
        result = await session.execute(
            select(PersonalWord).where(
                PersonalWord.user_id == callback.from_user.id,
                PersonalWord.is_learned == False
            )
        )
        words = result.scalars().all()
        if not words:
            await callback.message.edit_text('Ура! Все слова изучены!')
            return

    word = random.choice(words)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Показать перевод', callback_data=f'show_trans_{word.id}'))
    await callback.message.edit_text(f'Как переводится?\n\n **{word.word}**',reply_markup=builder.as_markup(),
                                     parse_mode='Markdown')

@router.callback_query(F.data.startswith('show_trans_'))
async def show_trans_with_choice(callback: CallbackQuery):
    word_id = int(callback.data.split('_')[2])
    async with SessionLocal() as session:
        word = await session.get(PersonalWord, word_id)
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text='✅ Помню', callback_data=f'word_up_{word_id}'),
            InlineKeyboardButton(text='❌ Забыл', callback_data=f'word_down_{word_id}'),
        )
        await callback.message.edit_text(
            f'Слово: **{word.word}**\nПеревод: **{word.translation}**',
            reply_markup=builder.as_markup(), parse_mode='Markdown'
        )

@router.callback_query(F.data.startswith('word_'))
async def handle_word_progress(callback: CallbackQuery):
    parts = callback.data.split('_')
    is_remembered = (parts[1] == 'up')
    word_id = int(parts[2])
    # await update_word_progress(word_id, is_remembered)
    await show_dict_cards(callback)
