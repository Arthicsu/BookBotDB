from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    if current_page > 1:
        kb_builder.add(InlineKeyboardButton(
            text=LEXICON['backward'],
            callback_data='backward'
        ))

    kb_builder.add(InlineKeyboardButton(
        text=f'{current_page}/{total_pages}',
        callback_data=str(current_page)
    ))

    if current_page < total_pages:
        kb_builder.add(InlineKeyboardButton(
            text=LEXICON['forward'],
            callback_data='forward'
        ))

    return kb_builder.as_markup()
