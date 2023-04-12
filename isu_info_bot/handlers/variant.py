import os

from aiogram import types

from isu_info_bot import config
from isu_info_bot.handlers.images import merge_images
from isu_info_bot.handlers.keyboards import get_pagination_keyboard, get_current_page_index
from isu_info_bot.services.students import get_students_by_variant
from isu_info_bot.templates import render_template


async def variant(message: types.Message):
    args = message.text.split()[1:4]
    pages = await get_students_by_variant(*args)
    images = []
    for _, image, in pages[1].values():
        images.append(f'{config.BASE_DIR}/{image}')
    filename = await merge_images(images)
    photo = open(filename, 'rb')
    if len(pages) > 1:
        await message.answer_photo(
            photo, caption=render_template('variant.j2', {'students': pages[1]}),
            reply_markup=get_pagination_keyboard(1, len(pages), config.VARIANT_CALLBACK_PATTERN, args)
            )
    else:
        await message.answer_photo(photo, caption=render_template('variant.j2', {'students': pages[1]}))
    os.remove(filename)


async def variant_button(query: types.CallbackQuery):
    args = eval("".join(query.data.split()[1:]))
    pages = await get_students_by_variant(*args)
    curr_page_index = get_current_page_index(query.data.split()[0], config.VARIANT_CALLBACK_PATTERN)
    images = []
    for _, image, in pages[curr_page_index].values():
        images.append(f'{config.BASE_DIR}/{image}')
    filename = await merge_images(images)
    photo = open(filename, 'rb')
    new_ph = types.InputMediaPhoto(photo, caption=render_template('variant.j2', {"students": pages[curr_page_index]}))
    await query.message.edit_media(
        new_ph,
        reply_markup=get_pagination_keyboard(curr_page_index, len(pages), config.VARIANT_CALLBACK_PATTERN, args)
        )
    os.remove(filename)
