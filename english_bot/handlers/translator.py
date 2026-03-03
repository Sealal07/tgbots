from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from deep_translator import GoogleTranslator
from utils.keyboards import translation_inline
from database.engine import add_to_personal_dict
from aiogram.types import Message, CallbackQuery
import langdetect

router = Router()

# определяем состояние для переводчика
class TranslatorStates(StatesGroup):
    waiting_for_text = State()

@router.message(F.text == '🔄 Переводчик')
async def ask_translation(message: Message, state: FSMContext):
    await message.answer('Пришли слово или фразу на английском или русском языке')
    await state.set_state(TranslatorStates.waiting_for_text)

@router.message(TranslatorStates.waiting_for_text)
async def translate_text(message: Message, state: FSMContext):
    if message.text in ['📝 Тесты', '📚 Мой словарь', '� Идиома дня', '📊 Мой прогресс']:
        await state.clear()
        return

    try:
        source_lang = langdetect.detect(message.text)
    except:
        source_lang = 'en'
    if source_lang == 'ru':
        translated = GoogleTranslator(source='ru', target='en').translate(message.text)
        word = translated
        translation = message.text
    else:
        translated = GoogleTranslator(source='auto', target='ru').translate(message.text)
        word = message.text
        translation = translated
    if translated.lower() == message.text.lower():
        translated = GoogleTranslator(source='ru', target='en').translate(message.text)
        word = translated
        translation = message.text

    await message.answer(
        f'Перевод: {translated}',
        reply_markup=translation_inline(word, translation)
    )

@router.callback_query(F.data.startswith('add_'))
async def add_word_callback(callback: CallbackQuery):
    parts = callback.data.split('_', 2)
    word = parts[1]
    translation = parts[2]
    await  add_to_personal_dict(callback.from_user.id, word, translation)
    await callback.answer(f'Слово "{word}" добавлено!')
    await callback.message.edit_reply_markup(reply_markup=None)


