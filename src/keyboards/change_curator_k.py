import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_all_items_from_change_curator_k(items: list[dict], key: str, id):
    rows = [[InlineKeyboardButton(text=item[key], callback_data=str(item[id]))] for item in items]
    rows.append([InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=rows)


