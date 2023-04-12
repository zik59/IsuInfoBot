from aiogram import types


async def process_any_message(message: types.Message):
    await message.answer("Попробуйте /help")
