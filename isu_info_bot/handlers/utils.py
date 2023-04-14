import os

from aiogram import types
from PIL import Image

from isu_info_bot import config
from isu_info_bot.handlers.keyboards import get_pagination_keyboard, get_current_page_index
from isu_info_bot.templates import render_template


async def merge_images(images: list) -> str:
    images = [Image.open(x) for x in images]
    images = [i.resize((164, 250)) for i in images]
    if len(images) <= 5:
        width = images[0].size[0]*len(images)
        height = images[0].size[1]
    else:
        width = images[0].size[0]*5
        height = images[0].size[1]*2
    new_image = Image.new('RGB', (width, height))
    x_offset = 0
    y_offset = 0
    for i, image in enumerate(images):
        if i == 5:
            x_offset = 0
            y_offset = image.size[1]
        new_image.paste(image, (x_offset, y_offset))
        x_offset += images[i].size[0]
    filename = f'{config.BASE_DIR}/images/test.jpg'
    new_image.save(filename)
    return filename


async def extract_images_from_page(pages: dict, curr_page_index: int = 1) -> list:
    images = []
    for _, image, in pages[curr_page_index].values():
        images.append(f'{config.BASE_DIR}/{image}')
    return images


async def get_file_with_photo(pages: dict, curr_page_index: int = 1) -> str:
    images = await extract_images_from_page(pages, curr_page_index)
    filename = await merge_images(images)
    return filename


async def send_answer(message: types.Message,
                      pages: dict,
                      template: str,
                      callback_pattern: str,
                      *args):
    filename = await get_file_with_photo(pages)
    photo = open(filename, 'rb')
    if len(pages) > 1:
        await message.answer_photo(
            photo, caption=render_template(template, {'students': pages[1]}),
            reply_markup=get_pagination_keyboard(1, len(pages), callback_pattern, *args)
            )
    else:
        await message.answer_photo(photo, caption=render_template(template, {'students': pages[1]}))
    os.remove(filename)


async def edit_answer(query: types.CallbackQuery,
                      pages: dict,
                      template: str,
                      callback_pattern: str,
                      *args):
    curr_page_index = get_current_page_index(query.data.split()[0], callback_pattern)
    filename = await get_file_with_photo(pages, curr_page_index)
    photo = open(filename, 'rb')
    new_photo = types.InputMediaPhoto(photo, caption=render_template(template, {"students": pages[curr_page_index]}))
    await query.message.edit_media(
        new_photo,
        reply_markup=get_pagination_keyboard(curr_page_index, len(pages), callback_pattern, *args)
        )
    os.remove(filename)
