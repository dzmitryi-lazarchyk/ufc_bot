from datetime import datetime
from time import strptime, mktime
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, tostring

from tgbot.models.custom_models import News


async def get_news():
    u = urlopen(r'https://www.championat.com/rss/news/boxing/')
    doc = parse(u)
    all_news=[]
    for item in doc.iterfind('channel/item'):
        categories = item.iterfind('category')
        for category in categories:
            if category.text == 'breaking':
                struct_object= strptime(item.findtext('pubDate'),'%a, %d %b %Y %H:%M:%S %z')
                pubDate = datetime.fromtimestamp(mktime(struct_object))
                image = item.find('image')
                if image:
                    image_url=image.findtext('url')
                else:
                    image_url=None
                news = News(title= item.findtext('title'),
                            link=item.findtext('link'),
                            pubDate = pubDate,
                            description = item.findtext('description').translate(item.findtext('description').maketrans('\n',' ')),
                            image = image_url,
                            )
                all_news.append(news)
                break
    # for news in all_news:
    #     print(f'{news.title}\n'
    #           f'{news.description}\n'
    #           f'{news.link}\n'
    #           f'{type(news.pubDate)}\n\n')
    return all_news
