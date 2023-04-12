import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from isu_info_bot import config, handlers
from isu_info_bot.handlers.variant import register_handlers_variant
from isu_info_bot.handlers.group import register_handlers_group
from isu_info_bot.handlers.student import register_handlers_student


COMMAND_HANDLERS = {
    'start': handlers.start,
    'help': handlers.help_,
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not config.TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN env variable "
        "wasn't implemented in .env (should be initialized)."
    )


def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    storage = RedisStorage2()
    dp = Dispatcher(bot, storage=storage)
    register_handlers_variant(dp)
    register_handlers_group(dp)
    register_handlers_student(dp)
    for command_name, command_handler in COMMAND_HANDLERS.items():
        dp.register_message_handler(command_handler, commands=[command_name])

    dp.register_message_handler(handlers.process_any_message)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
