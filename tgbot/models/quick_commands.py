from tgbot.models.custom_models import News


async def select_all_news():
    all_news = await News.query.gino.all()
    return all_news

async def pick_new_news(new_news:set):
    old_news = set(await News.query.gino.all())
    result = new_news-old_news
    if result:
        await News.delete.gino.all()
        for news in new_news:
            news.create()
    return result
