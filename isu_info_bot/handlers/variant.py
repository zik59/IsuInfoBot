from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from isu_info_bot import config
from isu_info_bot.handlers.keyboards import get_faculty_keyboard
from isu_info_bot.handlers.utils import send_answer, edit_answer
from isu_info_bot.services.students import get_students_by_variant


callback_pattern = config.VARIANT_CALLBACK_PATTERN
pattern = rf"^{callback_pattern}(\d+)."
template = 'variant.j2'

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
    await message.answer("Выберите факультет", reply_markup=get_faculty_keyboard())


async def faculty_chosen(message: types.Message, state: FSMContext):
    if message.text.isnumeric():
        faculty = message.text
    else:
        faculty = faculties[message.text]
    await state.update_data(chosen_faculty=faculty)
    await state.set_state(Variant.course.state)
    await message.answer("Введите курс", reply_markup=ReplyKeyboardRemove())


async def variant(message: types.Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer("Курсом должно быть число")
        return
    user_data = await state.get_data()
    args = user_data['chosen_variant'], user_data['chosen_faculty'], message.text
    pages = await get_students_by_variant(*args)
    if not pages:
        await message.answer("По вашему запросу ничего не найдено")
        await state.finish()
        return
    await send_answer(message, pages, template, callback_pattern, args)
    await state.finish()


async def variant_button(query: types.CallbackQuery):
    args = eval("".join(query.data.split()[1:]))
    pages = await get_students_by_variant(*args)
    await edit_answer(query, pages, template, callback_pattern, args)


def register_handlers_variant(dp: Dispatcher) -> None:
    dp.register_message_handler(variant_start, commands="variant", state=None)
    dp.register_message_handler(variant_chosen, state=Variant.variant)
    dp.register_message_handler(faculty_chosen, state=Variant.faculty)
    dp.register_message_handler(variant, state=Variant.course)
    dp.register_callback_query_handler(variant_button, Regexp(regexp=pattern).check, state="*")
