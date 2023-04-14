from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State

from isu_info_bot import config
from isu_info_bot.handlers.utils import send_answer, edit_answer
from isu_info_bot.services.students import get_students_by_name

callback_pattern = config.STUDENT_CALLBACK_PATTERN
pattern = rf"^{callback_pattern}(\d+)."
template = 'student.j2'


class Student(StatesGroup):
    student = State()


async def student_start(message: types.Message, state: FSMContext):
    await message.answer("Введите имя")
    await state.set_state(Student.student.state)


async def student(message: types.Message, state: FSMContext):
    name = message.text
    pages = await get_students_by_name(name)
    if not pages:
        await message.answer("По вашему запросу ничего не найдено, попробуйте ввести другое имя")
        return
    await send_answer(message, pages, template, callback_pattern, name)
    await state.finish()


async def student_button(query: types.CallbackQuery):
    name = " ".join(query.data.split()[1:])
    pages = await get_students_by_name(name)
    await edit_answer(query, pages, template, callback_pattern, name)


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(student_start, commands="student", state=None)
    dp.register_message_handler(student, state=Student.student)
    dp.register_callback_query_handler(student_button, Regexp(regexp=pattern).check, state="*")
