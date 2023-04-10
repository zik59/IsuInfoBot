from aiogram import types

from isu_info_bot import config
from isu_info_bot.handlers.keyboards import get_pagination_keyboard, get_current_page_index
from isu_info_bot.services.students import get_group_by_name
from isu_info_bot.templates import render_template


async def show_group_by_name(message: types.Message):
    name = " ".join(message.text.split()[1:])
    pages = get_group_by_name(name)
    if len(pages) > 1:
        await message.answer(
            render_template('group.j2', {'groups': pages[1]}),
            reply_markup=get_pagination_keyboard(1, len(pages), config.GROUP_CALLBACK_PATTERN, name)
            )
    else:
        await message.answer(render_template('group.j2', {'groups': pages[1]}))


async def group_button(query: types.CallbackQuery):
    name = " ".join(query.data.split()[1:])
    pages = get_group_by_name(name)
    curr_page_index = get_current_page_index(query.data.split()[0], config.GROUP_CALLBACK_PATTERN)
    await query.message.edit_text(
        render_template('group.j2', {"groups": pages[curr_page_index]}),
        reply_markup=get_pagination_keyboard(curr_page_index, len(pages), config.GROUP_CALLBACK_PATTERN, name)
        )
