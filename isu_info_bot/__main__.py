import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from isu_info_bot import config, handlers


REGISTER = [
    handlers.register_handlers_cancel,
    handlers.register_handlers_help,
    handlers.register_handlers_start,
    handlers.register_handlers_variant,
    handlers.register_handlers_group,
    handlers.register_handlers_student,
    handlers.register_handlers_process_any
]

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


def register_all_handlers(dp: Dispatcher) -> None:
    for elem in REGISTER:
        elem(dp)


def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    storage = RedisStorage2()
    dp = Dispatcher(bot, storage=storage)
    register_all_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
