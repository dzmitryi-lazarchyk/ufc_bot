import requests
from bs4 import BeautifulSoup

from tgbot.models.custom_models import Fighters

url = "https://www.ufc.com"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "W/\"1682055209\"",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"}


async def get_fighter_info(link):
    data = dict()
    page = requests.get(url=url+link, headers=headers)
    # print(page.status_code)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup.span.unwrap()

    data['image'] = soup.find("meta", attrs={"property": "og:image"}).get("content")

    nickname = soup.find("p", attrs={"class": "hero-profile__nickname"})
    data['nickname'] = nickname.text if nickname else None

    data['wins_loses'] = soup.find("p", attrs={"class": "hero-profile__division-body"}).text
    stats = soup.find_all("div", attrs={"class": "hero-profile__stat"})
    data['stats'] = dict()
    for stat in stats:
        text = stat.find("p", attrs={"class": "hero-profile__stat-text"}).text
        numb = stat.find("p", attrs={"class": "hero-profile__stat-numb"}).text
        data['stats'].update({text: numb})
    data['last_fight']={
        'event': soup.find("div", attrs={"class": "c-card-event--athlete-fight__logo"}).find("h2").text,
        'headline': soup.find("h3", attrs={"class": "c-card-event--athlete-fight__headline"}).text.strip(),
        'date': soup.find("div", attrs={"class": "c-card-event--athlete-fight__date"}).text.strip(),
    }
    return data


async def renew_rankings():
    page = requests.get(url=url+"/rankings", headers=headers)
    if page.status_code == 200:
        await Fighters.delete.gino.all()
        soup = BeautifulSoup(page.text, 'html.parser')
        rankings = soup.find_all(name="div", attrs={"class": "view-grouping"})
        fighters = []
        for ranking in rankings:
            division = ranking.find(name="div", attrs={"class": "view-grouping-header"})
            # Get rid of top ranks
            if "Top Rank" in division.text:
                continue
            else:
                pass
                # Champion
                name = ranking.find("h5").text
                rank = ranking.find("h6").text.strip()
                division = ranking.find("h4").text
                link = ranking.find("h5").find("a").get(key="href")
                fighter_info = await get_fighter_info(link=link)
                fighter = Fighters(
                    name=name,
                    link=url+link,
                    rank=rank,
                    division=division,
                    image=fighter_info['image'],
                    nickname=fighter_info['nickname'],
                    wins_loses=fighter_info['wins_loses'],
                    stats=fighter_info['stats'],
                    last_fight_event=fighter_info['last_fight']['event'],
                    last_fight_date=fighter_info['last_fight']['date'],
                    last_fight_headline=fighter_info['last_fight']['headline'],
                )
                await fighter.create()
                # Other fighters
                for row in ranking.find_all("tr"):
                    name = row.find("td", attrs={"class": "views-field views-field-title"}).text
                    link = row.find("td", attrs={"class": "views-field views-field-title"}).find("a").get(key="href")
                    rank = row.find("td", attrs={"class": "views-field views-field-weight-class-rank"}).text.strip()

                    fighter_info = await get_fighter_info(link=link)
                    fighter = Fighters(
                        name=name,
                        link=url+link,
                        rank=rank,
                        division=division,
                        image=fighter_info['image'],
                        nickname=fighter_info['nickname'],
                        wins_loses=fighter_info['wins_loses'],
                        stats=fighter_info['stats'],
                        last_fight_event=fighter_info['last_fight']['event'],
                        last_fight_date=fighter_info['last_fight']['date'],
                        last_fight_headline=fighter_info['last_fight']['headline'],
                    )
                    await fighter.create()

