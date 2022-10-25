import asyncio

from tgbot.config import load_config
from tgbot.misc.get_news import get_news
# from tgbot.models import quick_commands
from tgbot.models.base_models import db
from tgbot.models.custom_models import News

db_config = load_config().db
POSTGRES_URI=f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}"

async def test():
    await db.set_bind(POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    all_news = get_news()
    for news in all_news:
        await news.create()

    news = await News.query.gino.all()
    print(f"all users:{news}")
    await News.delete.gino.all()
    news = await News.query.gino.all()
    print(f"all users:{news}")


loop = asyncio.new_event_loop()

loop.run_until_complete(test())