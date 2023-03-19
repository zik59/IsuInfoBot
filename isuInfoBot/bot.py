from aiogram import Bot, Dispatcher, executor, types

API_TOKEN  = '6127246448:AAGXVDbsxS_EQskTZVOpciM8VUBzELzfgV8'

bot = Bot(toketn=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ IsuInfoBot, могу найти из какой группы человек или какой у него вариант по ису")

@dp.message_handler(commands=['help'])
async def give_help(message: types.Message)
    await message.reply() #To do

@dp.message_handler()
async def give_advice(message: types.Message)
    await message.reply() #To do

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)