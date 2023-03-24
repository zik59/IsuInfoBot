from aiogram import types

from isu_info_bot.services.students import get_students_by_variant
from isu_info_bot.templates import render_template

async def variant(message: types.Message):
    variant = message.text.partition(" ")[2]
    await message.answer(render_template('variant.j2',
                            {"students": get_students_by_variant(int(variant))}))
