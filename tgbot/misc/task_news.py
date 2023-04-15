import asyncio
import datetime

import aioschedule as aioschedule
from aiogram import Dispatcher

from tgbot.config import load_config
from tgbot.misc.get_news import get_news_championat
from tgbot.models.quick_commands import pick_new_news, select_all_news


async def news(dp:Dispatcher):
    parse_news = await get_news_championat()
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
                new_news = sorted(new_news, key=lambda x: x.pubDate)
                for news in new_news:
                    if news.image:
                        await dp.bot.send_photo(chat_id=chat_id, photo=news.image,
                                                caption=f'<b>{news.title}</b>\n' \
                                                        f'<i>{news.pubDate.strftime("%d.%m %H:%M")}</i>\n\n' \
                                                        f'{news.description}\n\n' \
                                                        f'Подробнее:{news.link}\n\n')
                    else:
                        await dp.bot.send_message(chat_id=chat_id,
                                                  text=f'<b>{news.title}</b>\n' \
                                                       f'<i>{news.pubDate.strftime("%d.%m %H:%M")}</i>\n\n' \
                                                       f'{news.description}\n' \
                                                       f'Подробнее:{news.link}\n\n',
                                                  disable_web_page_preview=True)




async def scheduler(dp:Dispatcher):
    await news(dp)
    aioschedule.every().day.at('09:00').do(news, dp)
    aioschedule.every().day.at('12:00').do(news, dp)
    aioschedule.every().day.at('15:00').do(news, dp)
    aioschedule.every().day.at('18:00').do(news, dp)
    aioschedule.every().day.at('20:00').do(news, dp)
    aioschedule.every().days()

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)