from aiogram import types

from services.students import get_group_by_name


async def show_group_by_name(message: types.Message):
    name = message.text.partition(" ")[2]
    await message.reply(get_group_by_name(name))
