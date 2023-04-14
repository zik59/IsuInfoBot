from aiogram import Dispatcher, types

from isu_info_bot.templates import render_template


async def start(message: types.Message):
    await message.answer(render_template('start.j2'))


def register_handlers_start(dp: Dispatcher) -> None:
    dp.register_message_handler(start, commands=['start'], state=None)
