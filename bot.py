import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from gino import Gino

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.my_middleware import MyMiddleware, ACLMiddleware
from tgbot.misc.tasks import scheduler
from tgbot.models.base_models import db
from web_app.keep_alive import keep_alive

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(MyMiddleware())
    dp.setup_middleware(ACLMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    # register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    await dp.bot.set_my_commands([
        types.bot_command.BotCommand('start', 'Запустить бота'),
        types.bot_command.BotCommand('rankings', 'Рейтинги бойцов'),
        types.bot_command.BotCommand('upcoming_events', 'Предстоящие турниры'),
        types.bot_command.BotCommand('past_events', 'Прошедшие турниры'),
        types.bot_command.BotCommand('settings_news', 'Настроить новости')
    ])


    POSTGRES_URI = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}"

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await db.set_bind(POSTGRES_URI)
        await db.gino.create_all()
        asyncio.create_task(scheduler(dp))
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.close()


if __name__ == '__main__':
    try:
        print("Starting")
        keep_alive()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
