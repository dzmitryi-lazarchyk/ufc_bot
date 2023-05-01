from tgbot.models.custom_models import News, Fighters


async def select_all_news():
    all_news = await News.query.gino.all()
    return all_news

async def pick_new_news(new_news:set):
    old_news = await News.query.gino.all()
    old_news_titles = set([news.title for news in old_news])
    new_news_titles = set([news.title for news in new_news])

    result_titles = new_news_titles-old_news_titles
    result = [news for news in new_news if news.title in result_titles]

    if result:
        # Sort by date
        result.sort(key=lambda news: news.pubDate)

        await News.delete.gino.all()
        for news in new_news:
            await news.create()
    # Send no more than 5 news
    if len(result) > 5:
        return result[-5:]
    else:
        return result


async def get_rankings():
    all_fighters = await Fighters.query.gino.all()
    return all_fighters


