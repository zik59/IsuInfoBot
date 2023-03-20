import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from services.students import get_group_by_name, get_students_by_variant

load_dotenv()

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('''Привет!\nЯ IsuInfoBot, могу найти из какой группы человек\nили найти людей по номеру варианта на ису''')


@dp.message_handler(commands=['help'])
async def give_help(message: types.Message):
    await message.reply('''По запросу /group можно получить из какой группы человек\nПо запросу /variant можно получить список людей с заданным вариантом''') 


@dp.message_handler(commands=['group'])
async def show_group_by_name(message: types.Message):
    name = message.text.partition(" ")[2]
    await message.reply(get_group_by_name(name))


@dp.message_handler(commands=['variant'])
async def show_people_by_isu_number(message: types.Message):
    variant = message.text.partition(" ")[2]
    await message.reply(get_students_by_variant(int(variant)))


@dp.message_handler()
async def give_advice(message: types.Message):
    await message.reply('Пошел нахер вонючка\nПопробуй /help')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)