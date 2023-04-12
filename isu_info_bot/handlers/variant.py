import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from isu_info_bot import config
from isu_info_bot.handlers.images import merge_images
from isu_info_bot.handlers.keyboards import get_pagination_keyboard, get_current_page_index
from isu_info_bot.services.students import get_students_by_variant
from isu_info_bot.templates import render_template


pattern = rf"^{config.VARIANT_CALLBACK_PATTERN}(\d+)."

faculties = {'фкио': 1,
             'машфак': 2,
             'фмп': 3,
             'экономфак': 4,
             'специалитет фкио, машфака и фмп': 5,
             'специалитет фкио': 6,
             'фенго': 7,
             'фцпт': 20,
             'колледж': 8,
             'аспирантура': 9
             }


class Variant(StatesGroup):
    variant = State()
    faculty = State()
    course = State()


async def variant_start(message: types.Message, state: FSMContext):
    await message.answer("Введите вариант")
    await state.set_state(Variant.variant.state)


async def variant_chosen(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer("Вариантом должно быть число")
        return
    await state.update_data(chosen_variant=message.text)
    await state.set_state(Variant.faculty.state)
    keyboard = [
        [KeyboardButton('фкио'), KeyboardButton('машфак'), KeyboardButton('фмп')],
        [KeyboardButton('экономфак'), KeyboardButton('специалитет фкио, машфака и фмп'), KeyboardButton('специалитет фкио')],
        [KeyboardButton('фенго'), KeyboardButton('колледж'), KeyboardButton('аспирантура')]
    ]
    await message.answer("Выберите факультет", reply_markup=ReplyKeyboardMarkup(keyboard))


async def faculty_chosen(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        faculty = message.text
    else:
        faculty = faculties[message.text]
    await state.update_data(chosen_faculty=faculty)
    await state.set_state(Variant.course.state)
    await message.answer("Введите курс")


async def variant(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer("Курсом должно быть число")
        return
    user_data = await state.get_data()
    args = user_data['chosen_variant'], user_data['chosen_faculty'], message.text
    pages = await get_students_by_variant(*args)
    if not pages:
        await message.answer("По вашему запросу ничего не найдено")
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
    await state.finish()


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


def register_handlers_variant(dp: Dispatcher) -> None:
    dp.register_message_handler(variant_start, commands="variant", state="*")
    dp.register_message_handler(variant_chosen, state=Variant.variant)
    dp.register_message_handler(faculty_chosen, state=Variant.faculty)
    dp.register_message_handler(variant, state=Variant.course)
    dp.register_callback_query_handler(variant_button, Regexp(regexp=pattern).check, state="*")
