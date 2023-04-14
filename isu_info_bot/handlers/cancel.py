from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


async def cancel(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())


def register_handlers_cancel(dp: Dispatcher) -> None:
    dp.register_message_handler(cancel, commands="cancel", state="*")
