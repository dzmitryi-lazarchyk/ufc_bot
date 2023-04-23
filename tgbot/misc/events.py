import requests
from bs4 import BeautifulSoup

from tgbot.models.custom_models import Events, UpcomingMatches

url = "https://www.espn.com/mma/schedule/_/league/ufc"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "W/\"1682221752\"",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  }

async def get_upcoming_matches(link, event):
    page = requests.get(url=link, headers=headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        sections = soup.find_all(name="section", attrs={"class": "Card MMAFightCard"})
        for section in sections:
            card = section.find(name="h3", attrs={"class": "Card__Header__Title Card__Header__Title--no-theme"}).text
            matches = section.find_all(name="div", attrs={"class": "MMAGamestrip flex items-center justify-center"})
            for match in matches:
                competitors = match.find_all(name="div",
                                             attrs={"class": "MMACompetitor__Detail flex flex-column justify-center"})
                cnt = 1
                for competitor in competitors:
                    if cnt == 1:
                        first_competitor = competitor.find(name="h2").text
                        first_competitor_wins_loses = competitor.find(name="div").text if competitor.find(name="div")\
                            else None
                        cnt += 1
                    else:
                        second_competitor = competitor.find(name="h2").text
                        second_competitor_wins_loses = competitor.find(name="div").text if competitor.find(name="div")\
                            else None
                match_number = match.find(name="div", attrs={
                    "class": "ScoreCell__ScoreDate Gamestrip__ScoreDate clr-gray-04 h9"}).text
                match_number = int(match_number.strip().strip("Match "))

                odds = match.find(name="div", attrs={"class": "ScoreCell__Odds Gamestrip__Odds clr-gray-03 n9"}).text \
                    if match.find(name="div", attrs={"class": "ScoreCell__Odds Gamestrip__Odds clr-gray-03 n9"}) else None

                match = UpcomingMatches(
                    card=card,
                    first_competitor=first_competitor,
                    first_competitor_wins_loses=first_competitor_wins_loses,
                    second_competitor=second_competitor,
                    second_competitor_wins_loses=second_competitor_wins_loses,
                    match_number=match_number,
                    odds=odds,
                    event_title=event.title,
                )
                await match.create()


async def events():
    page = requests.get(url=url, headers=headers)
    if page.status_code == 200:
        await Events.delete.gino.all()
        soup = BeautifulSoup(page.text, 'html.parser')
        tables = soup.find_all(name="div", attrs={"class":"ResponsiveTable"})
        for table in tables:
            table_title = table.find(name="div", attrs={"class":"Table__Title"}).text
            events = table.find_all(name="tr", attrs={"class": "Table__TR Table__TR--sm Table__even"})
            for event in events:
                date = event.find(name="td", attrs={"class": "date__col Table__TD"}).text
                title = event.find(name="td", attrs={"class": "event__col Table__TD"}).text
                link = "https://www.espn.com" + event.find(name="a", attrs={"class": "AnchorLink"}).get("href")
                location = event.find(name="td", attrs={"class": "location__col Table__TD"}).text or "Unknown"
                match table_title:
                    case "Scheduled Events" | "This Week's Events":
                        event_obj = Events(
                            date=date,
                            title=title,
                            location=location,
                            link=link,
                            status="Upcoming",
                        )
                        await event_obj.create()

                        await get_upcoming_matches(link, event_obj)
                    case "Past Results":
                        event_obj = Events(
                            date=date,
                            title=title,
                            location=location,
                            link=link,
                            status="Past",
                        )
                        await event_obj.create()



