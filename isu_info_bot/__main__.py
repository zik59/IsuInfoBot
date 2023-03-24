import logging

from aiogram import Bot, Dispatcher, executor

from isu_info_bot import config, handlers


COMMAND_HANDLERS = {
    'start': handlers.start,
    'help': handlers.help_,
    'group': handlers.show_group_by_name,
    'variant': handlers.variant
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

if not config.TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN env variable "
        "wasn't implemented in .env (should be initialized)."
    )


def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)

    for command_name, command_handler in COMMAND_HANDLERS.items():
        dp.register_message_handler(command_handler, commands=[command_name])

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
