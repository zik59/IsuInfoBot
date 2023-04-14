from aiogram import Dispatcher, types

from isu_info_bot.templates import render_template


async def help_(message: types.Message):
    await message.answer(render_template('help.j2'))


def register_handlers_help(dp: Dispatcher) -> None:
    dp.register_message_handler(help_, commands="help", state=None)
