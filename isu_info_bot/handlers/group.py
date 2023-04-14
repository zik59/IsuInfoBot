from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters.state import StatesGroup, State

from isu_info_bot import config
from isu_info_bot.handlers.utils import send_answer, edit_answer
from isu_info_bot.services.students import get_students_by_group


callback_pattern = config.GROUP_CALLBACK_PATTERN
pattern = rf"^{callback_pattern}(\d+)."
template = 'group.j2'


class Group(StatesGroup):
    group = State()


async def group_start(message: types.Message, state=FSMContext):
    await message.answer("Введите номер группы")
    await state.set_state(Group.group.state)


async def group(message: types.Message, state=FSMContext):
    group = message.text
    pages = await get_students_by_group(group)
    if not pages:
        await message.answer("По вашему запросу ничего не найдено, попробуйте ввести другой номер группы")
        return
    await send_answer(message, pages, template, callback_pattern, group)
    await state.finish()


async def group_button(query: types.CallbackQuery):
    group = " ".join(query.data.split()[1:])
    pages = await get_students_by_group(group)
    await edit_answer(query, pages, template, callback_pattern, group)


def register_handlers_group(dp: Dispatcher) -> None:
    dp.register_message_handler(group_start, commands="group", state=None)
    dp.register_message_handler(group, state=Group.group)
    dp.register_callback_query_handler(group_button, Regexp(regexp=pattern).check, state="*")
