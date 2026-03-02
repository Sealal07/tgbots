from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    kb = [
        [KeyboardButton(text='📝 Тесты'), KeyboardButton(text='📚 Мой словарь')],
        [KeyboardButton(text='🔄 Переводчик'), KeyboardButton(text='� Идиома дня')],
        [KeyboardButton(text='📊 Мой прогресс')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def translation_inline(word, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить в словарь', callback_data=f'add_{word}_{translation}')]
    ])

def quiz_levels():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='A1-A2', callback_data='quiz_A1'),
         InlineKeyboardButton(text='B1-B2', callback_data='quiz_B1')]
    ])