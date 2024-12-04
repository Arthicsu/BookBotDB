from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import get_user_data, update_user_page, update_user_bookmarks
from filters.filters import IsDigitCallbackData
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    user_data = get_user_data(message.from_user.id)
    await message.answer(LEXICON[message.text])

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    update_user_page(message.from_user.id, 1)
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            current_page=1,
            total_pages=len(book)
        )
    )

@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    user_data = get_user_data(message.from_user.id)
    current_page = user_data['page']
    text = book[current_page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            current_page=current_page,
            total_pages=len(book)
        )
    )

@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    user_data = get_user_data(message.from_user.id)
    if user_data['bookmarks']:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_keyboard(
                *user_data['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    user_data = get_user_data(callback.from_user.id)
    current_page = user_data['page']
    if current_page < len(book):
        current_page += 1
        update_user_page(callback.from_user.id, current_page)
        text = book[current_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                current_page=current_page,
                total_pages=len(book)
            )
        )
    await callback.answer()

@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    user_data = get_user_data(callback.from_user.id)
    current_page = user_data['page']
    if current_page > 1:
        current_page -= 1
        update_user_page(callback.from_user.id, current_page)
        text = book[current_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                current_page=current_page,
                total_pages=len(book)
            )
        )
    await callback.answer()

@router.callback_query(IsDigitCallbackData())
async def process_page_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_page = int(callback.data)
    user_data = get_user_data(user_id)

    if not user_data:
        await callback.answer("Пользователь не найден в базе данных!")
        return

    user_data['bookmarks'].add(current_page)
    update_user_bookmarks(user_id, user_data['bookmarks'])

    await callback.answer('Страница добавлена в закладки!')
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    page = int(callback.data)
    update_user_page(callback.from_user.id, page)
    text = book[page]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            current_page=page,
            total_pages=len(book)
        )
    )

@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    user_data = get_user_data(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(
            *user_data['bookmarks']
        )
    )

@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])

@router.callback_query(lambda c: c.data.endswith('del') and c.data[:-3].isdigit())
async def process_del_bookmark_press(callback: CallbackQuery):
    user_data = get_user_data(callback.from_user.id)
    bookmark_to_remove = int(callback.data[:-3])
    bookmarks = user_data['bookmarks']
    bookmarks.discard(bookmark_to_remove)
    update_user_bookmarks(callback.from_user.id, bookmarks)
    if bookmarks:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *bookmarks
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
