from aiogram import types


async def help_(message: types.Message):
    await message.reply('''По запросу /group можно получить из какой группы человек\nПо запросу /variant можно получить список людей с заданным вариантом''')
