from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplayKeyboardMarkup, KeyKeyboardButton

langMenu = InlineKeyboardMarkup(row_width=2)

langRU = InlineKeyboardButton(text='Русский', callback_data='lang_ru')
langEN = InlineKeyboardButton(text='English', callback_data='lang_en')

langMenu.insert(langRU)
langMenu.insert(langEN)