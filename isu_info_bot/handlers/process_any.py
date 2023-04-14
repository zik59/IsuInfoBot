from aiogram import Dispatcher, types


async def process_any_message(message: types.Message):
    await message.answer("Попробуйте /help")


def register_handlers_process_any(dp: Dispatcher) -> None:
    dp.register_message_handler(process_any_message, state=None)
