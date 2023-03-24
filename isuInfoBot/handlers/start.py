from aiogram import types


async def start(message: types.Message):
    await message.reply('''Привет!\nЯ IsuInfoBot, могу найти из какой группы человек\nили найти людей по номеру варианта на ису''')
