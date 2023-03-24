from aiogram import types

from isu_info_bot.templates import render_template


async def start(message: types.Message):
    await message.answer(render_template('start.j2'))
