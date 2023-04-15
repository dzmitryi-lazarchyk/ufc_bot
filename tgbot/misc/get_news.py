import asyncio
from urllib import parse as prs
from datetime import datetime
from time import strptime, mktime
from urllib.request import urlopen,Request
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, tostring

from tgbot.models.custom_models import News


async def get_news_championat():
    u = urlopen(r'https://www.championat.com/rss/news/boxing/')
    # Check connection
    if u.status == 200:
        doc = parse(u)
        all_news=[]
        for item in doc.iterfind('channel/item'):
            categories = item.iterfind('category')
            for category in categories:
                if category.text == 'breaking':
                    struct_object= strptime(item.findtext('pubDate'),'%a, %d %b %Y %H:%M:%S %z')
                    pubDate = datetime.fromtimestamp(mktime(struct_object))
                    enclosure = item.find('enclosure')
                    try:
                        image_url = enclosure.get('url', default=None)
                    except AttributeError:
                        image_url = None
                    news = News(title= item.findtext('title'),
                                link=item.findtext('link'),
                                category=item.findall('category')[1].text,
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
    else:
        return None

async def get_news_bloodandsweat():
    url = r'https://www.bloodandsweat.ru/category/news/feed/'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    request = Request(url, None, headers)
    u = urlopen(request)
    # Check connection
    if u.status == 200:
        doc = parse(u)
        all_news=[]
        for item in doc.iterfind('channel/item'):
            struct_object= strptime(item.findtext('pubDate'),'%a, %d %b %Y %H:%M:%S %z')
            pubDate = datetime.fromtimestamp(mktime(struct_object))
            description = item.findtext('description')
            if len(description) > 250:
                description = description[:250] + "..."

            news = News(title=item.findtext('title'),
                        link=item.findtext('link'),
                        category=item.findtext('category'),
                        pubDate=pubDate,
                        description=item.findtext('description'),
                        image=None
                        )
            all_news.append(news)
        return all_news
    else:
        return None


