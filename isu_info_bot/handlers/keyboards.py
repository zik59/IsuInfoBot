from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def get_faculty_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton('фкио'), KeyboardButton('машфак'), KeyboardButton('фмп')],
        [KeyboardButton('экономфак'), KeyboardButton('специалитет фкио, машфака и фмп'), KeyboardButton('специалитет фкио')],
        [KeyboardButton('фенго'), KeyboardButton('колледж'), KeyboardButton('аспирантура')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_cancellation_keyboard() -> ReplyKeyboardMarkup:
    cancel = [[KeyboardButton('Отмена')]]
    return ReplyKeyboardMarkup(cancel, resize_keyboard=True)


def get_pagination_keyboard(
        curr_page_index: int, pages_count: int, callback_prefix: str, args
        ) -> InlineKeyboardMarkup:
    prev_index = curr_page_index - 1
    if prev_index < 1:
        prev_index = pages_count
    next_index = curr_page_index + 1
    if next_index > pages_count:
        next_index = 1
    keyboard = [
        [
            InlineKeyboardButton('<', callback_data=f'{callback_prefix}{prev_index} {args}'),
            InlineKeyboardButton(f'{curr_page_index}/{pages_count}', callback_data=' '),
            InlineKeyboardButton('>', callback_data=f'{callback_prefix}{next_index} {args}')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_current_page_index(query_data, callback_pattern) -> int:
    pattern_prefix_length = len(callback_pattern)
    return int(query_data[pattern_prefix_length:])
