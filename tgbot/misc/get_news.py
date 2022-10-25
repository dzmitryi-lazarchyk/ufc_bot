from urllib.request import urlopen
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, tostring

from tgbot.models.custom_models import News


def get_news():
    u = urlopen(r'https://www.championat.com/rss/news/boxing/')
    doc = parse(u)
    all_news=[]
    for item in doc.iterfind('channel/item'):
        categories = item.iterfind('category')
        for category in categories:
            if category.text == 'breaking':
                news = News(title= item.findtext('title'),
                            link=item.findtext('link'),
                            pubDate = item.findtext('pubDate'),
                            description = item.findtext('description'),
                            image = item.findtext('image'),
                            )
                all_news.append(news)
                break
    for news in all_news:
        print(f'{news.title}\n'
              f'{news.description}\n'
              f'{news.link}\n'
              f'{news.pubDate}\n\n')
    # s = {'name': 'Den', 'shares': 70, 'price': 345.23}
    # e = dict_to_xml('test', s)
    # with open('dict_xml.xml', 'wb') as file:
    #     file.write(tostring(e))
    # with open('dict_xml.xml', 'wb') as file:
    #     e.set('id', str(1234))
    #      file.write(tostring(e))
    # e = dict_to_xml_str('item', s)
    # print(e)
    # doc = parse('dict_xml.xml')
    # root = doc.getroot()
    # root.remove(root.find('shares'))
    # e = Element('spam')
    # e.text = 'fsdfdsf'
    # root.insert(1, e)
    # print(tostring(root))
    # doc.write('dict_xml.xml', xml_declaration=True)

get_news()