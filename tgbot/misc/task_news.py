import asyncio
import datetime
from time import gmtime

import aioschedule as aioschedule
from aiogram import Dispatcher
from pytz import timezone

from tgbot.config import load_config
from tgbot.misc.get_news import get_news_championat, get_news_bloodandsweat
from tgbot.misc.rankings import renew_rankings
from tgbot.models.quick_commands import pick_new_news, select_all_news

async def news(dp: Dispatcher):
    parse_news_championat = await get_news_championat()
    parse_news_bloodandsweat = await get_news_bloodandsweat()
    parse_news = parse_news_championat + parse_news_bloodandsweat
    if parse_news:
        new_news = await pick_new_news(parse_news)

        if new_news:
            chats = load_config().tg_bot.channels

            # *****************************ONE MESSAGE*************************

            # text = ''.join(f'<b>{news.title}</b>\n' \
            #                f'<i>{news.pubDate.strftime("%d.%m %H:%M")}</i>\n' \
            #                f'{news.description}\n' \
            #                f'Подробнее:{news.link}\n\n'
            #
            #                for news in new_news)
            # for chat in chats:
            #     if len(text) > 4096:
            #         for x in range(0, len(text), 4096):
            #             await dp.bot.send_message(chat_id=chat, text=text[x:x + 4096], disable_web_page_preview=True)
            #     else:
            #         await dp.bot.send_message(chat_id=chat, text=text, disable_web_page_preview=True)

            for chat_id in chats:
                for news in new_news:
                    print(news.pubDate)
                    if news.image:
                        await dp.bot.send_photo(chat_id=chat_id, photo=news.image,
                                                caption=f'<u>{news.category}</u>\n' 
                                                        f'<b>{news.title}</b>\n' 
                                                        f'<i>{news.pubDate.strftime("%d.%m %H:%M")}</i>\n\n' 
                                                        f'{news.description}\n\n'
                                                        f'Подробнее:{news.link}\n\n')
                    else:
                        await dp.bot.send_message(chat_id=chat_id,
                                                  text=f'<u>{news.category}</u>\n'
                                                       f'<b>{news.title}</b>\n'
                                                       f'<i>{news.pubDate.strftime("%d.%m %H:%M")}</i>\n\n'
                                                       f'{news.description}\n\n'
                                                       f'Подробнее:{news.link}\n\n',
                                                  disable_web_page_preview=True)


async def rankings():
    await renew_rankings()
async def scheduler(dp: Dispatcher):
    # await rankings()
    # await news(dp)
    for time in ('09:00','12:00','15:00','18:00','20:00'):
        aioschedule.every().tuesday.at(time).do(news, dp)
        aioschedule.every().wednesday.at(time).do(news, dp)
        aioschedule.every().thursday.at(time).do(news, dp)
        aioschedule.every().friday.at(time).do(news, dp)
        aioschedule.every().saturday.at(time).do(news, dp)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
