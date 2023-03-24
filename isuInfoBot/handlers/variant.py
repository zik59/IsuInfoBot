from aiogram import types

from services.students import get_students_by_variant


async def variant(message: types.Message):
    variant = message.text.partition(" ")[2]
    await message.reply(get_students_by_variant(int(variant)))
