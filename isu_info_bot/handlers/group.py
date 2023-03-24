from aiogram import types

from isu_info_bot.services.students import get_group_by_name
from isu_info_bot.templates import render_template

async def show_group_by_name(message: types.Message):
    name = message.text.partition(" ")[2]
    await message.answer(render_template('group.j2', {'groups': get_group_by_name(name)}))
