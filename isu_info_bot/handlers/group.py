import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State

from isu_info_bot import config
from isu_info_bot.handlers.images import merge_images
from isu_info_bot.handlers.keyboards import get_pagination_keyboard, get_current_page_index
from isu_info_bot.services.students import get_students_by_group
from isu_info_bot.templates import render_template


pattern = rf"^{config.GROUP_CALLBACK_PATTERN}(\d+)."


class Group(StatesGroup):
    group = State()


async def group_start(message: types.Message, state=FSMContext):
    await message.answer("Введите номер группы")
    await state.set_state(Group.group.state)


async def group(message: types.Message, state=FSMContext):
    group = message.text
    pages = await get_students_by_group(group)
    if not pages:
        await message.answer("По вашему запросу ничего не найдено")
    images = []
    for _, image, in pages[1].values():
        images.append(f'{config.BASE_DIR}/{image}')
    filename = await merge_images(images)
    photo = open(filename, 'rb')
    if len(pages) > 1:
        await message.answer_photo(
            photo, caption=render_template('group.j2', {'students': pages[1]}),
            reply_markup=get_pagination_keyboard(1, len(pages), config.GROUP_CALLBACK_PATTERN, group)
            )
    else:
        await message.answer_photo(photo, caption=render_template('group.j2', {'students': pages[1]}))
    os.remove(filename)
    await state.finish()


async def group_button(query: types.CallbackQuery):
    group = " ".join(query.data.split()[1:])
    pages = await get_students_by_group(group)
    curr_page_index = get_current_page_index(query.data.split()[0], config.GROUP_CALLBACK_PATTERN)
    images = []
    for _, image, in pages[curr_page_index].values():
        images.append(f'{config.BASE_DIR}/{image}')
    filename = await merge_images(images)
    photo = open(filename, 'rb')
    new_ph = types.InputMediaPhoto(photo, caption=render_template('group.j2', {"students": pages[curr_page_index]}))
    await query.message.edit_media(
        new_ph,
        reply_markup=get_pagination_keyboard(curr_page_index, len(pages), config.GROUP_CALLBACK_PATTERN, group)
        )
    os.remove(filename)


def register_handlers_group(dp: Dispatcher) -> None:
    dp.register_message_handler(group_start, commands="group", state="*")
    dp.register_message_handler(group, state=Group.group)
    dp.register_callback_query_handler(group_button, Regexp(regexp=pattern).check, state="*")
