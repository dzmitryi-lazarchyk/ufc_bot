from sqlalchemy import Column, String, DateTime,\
    Text, sql, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from tgbot.models.base_models import BaseModel


class Users(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    receive_news = Column(Boolean(), default=False)

    @classmethod
    async def get_Users(cls):
        users = await Users.query.gino.all()
        return users


class News(BaseModel):
    __tablename__ = 'news'
    title = Column(String(), primary_key=True)
    category = Column(String())
    link = Column(String())
    pubDate= Column(DateTime(timezone=False))
    description = Column(Text())
    image = Column(String())

    query: sql.Select

class Fighters(BaseModel):
    __tablename__ = 'fighters'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String())
    link = Column(String())
    division = Column(String())
    rank = Column(String())
    image = Column(String())
    nickname = Column(String())
    wins_loses = Column(String())
    stats = Column(JSONB())
    last_fight_event = Column(String())
    last_fight_date = Column(String())
    last_fight_headline = Column(String())


    def __str__(self):
        nickname = f"Nickname:<i>{self.nickname}</i>" if self.nickname else ""
        statistics = "\n".join([f"{key}:{value}" for key, value in self.stats.items()])

        text = f"<b>{self.rank}. {self.name}</b>\n"\
               f"{nickname}\n\n"\
               f"{self.wins_loses}\n\n"\
               f"Статистика:\n{statistics}\n\n"\
               f"Последний турнир:\n{self.last_fight_date},"\
               f" {self.last_fight_event}, {self.last_fight_headline}\n" \
               f"<a href='{self.link}'>Сайт UFC</a>"

        return text
    @classmethod
    async def get_champion(cls, division:str):
        champion = await Fighters.query.where(Fighters.division == division
                                              and Fighters.rank == "Champion").gino.first()

        return champion

    @classmethod
    async def get_fighter_by_name(cls, name:str):
        fighter = await Fighters.query.where(Fighters.name == name).gino.first()
        return fighter

    @classmethod
    async def get_division_fighters(cls, division:str):
        # Without a champion
        division_fighters = await Fighters.query.where(Fighters.division == division).gino.all()
        return division_fighters

    @classmethod
    async def get_division_fighter(cls, division: str, rank:str):
        fighter = await Fighters.query.where(Fighters.division == division).\
            where(Fighters.rank == rank).gino.first()
        return fighter

    @classmethod
    async def get_next_previous(cls, division: str, rank:str):
        # Get ranks
        division_fighters = await cls.get_division_fighters(division=division)
        ranks = [fighter.rank for fighter in division_fighters]
        # Get indexes of next and previous ranks
        indx_rank = ranks.index(rank)
        indx_next = indx_rank+1
        indx_prev = indx_rank-1
        # Get ranks
        try:
            next_rank = ranks[indx_next]
        except IndexError:
            next_rank = ranks[0]

        try:
            prev_rank = ranks[indx_prev]
        except IndexError:
            prev_rank = ranks[-1]

        return next_rank, prev_rank

    @classmethod
    async def get_all_ranks(cls, division: str):
        ranks = await Fighters.select("rank").where(Fighters.division == division).gino.all()
        ranks = [rank[0] for rank in ranks]
        return ranks


class Events(BaseModel):
    __tablename__='events'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    date = Column(String())
    event_title = Column(String(), unique=True)
    link = Column(String())
    location = Column(String())
    status = Column(String())

    def __str__(self):
        text = f"<a href='{self.link}'><b>{self.event_title}</b></a>\n" \
               f"<i>{self.date}</i>\n" \
               f"Место проведения: {self.location}"

        return text
    @classmethod
    async def get_upcoming_events(cls):
        upcoming_events = await Events.select("event_title").where(Events.status == "Upcoming").gino.all()
        upcoming_events = [event[0] for event in upcoming_events]
        return upcoming_events

    @classmethod
    async def get_first_upcoming_event(cls):
        first_event = await Events.query.where(Events.status == "Upcoming").gino.first()

        return first_event
    @classmethod
    async def get_event(cls, event_id:int):
        event = await Events.query.where(Events.id == event_id).gino.first()

        return event

    @classmethod
    async def get_next_previous_upcoming(cls, event_id: int):
        # Get events
        upcoming_events = await Events.select("id").where(Events.status == "Upcoming").gino.all()
        upcoming_events_ids = [event[0] for  event in upcoming_events]
        # Get indexes of next and previous events
        indx_event = upcoming_events_ids.index(event_id)
        indx_next = indx_event + 1
        indx_prev = indx_event - 1
        # Get ranks
        try:
            next_event = upcoming_events_ids[indx_next]
        except IndexError:
            next_event = upcoming_events_ids[0]

        try:
            prev_event = upcoming_events_ids[indx_prev]
        except IndexError:
            prev_event = upcoming_events_ids[-1]

        return next_event, prev_event

    @classmethod
    async def get_past_events(cls):
        upcoming_events = await Events.select("event_title").where(Events.status == "Past").gino.all()
        upcoming_events = [event[0] for event in upcoming_events]
        return upcoming_events

    @classmethod
    async def get_first_past_event(cls):
        first_event = await Events.query.where(Events.status == "Past").gino.first()

        return first_event

    @classmethod
    async def get_next_previous_past(cls, event_id: int):
        # Get events
        past_events = await Events.select("id").where(Events.status == "Past").gino.all()
        past_events_ids = [event[0] for event in past_events]
        # Get indexes of next and previous events
        indx_event = past_events_ids.index(event_id)
        indx_next = indx_event + 1
        indx_prev = indx_event - 1
        # Get ranks
        try:
            next_event = past_events_ids[indx_next]
        except IndexError:
            next_event = past_events_ids[0]

        try:
            prev_event = past_events_ids[indx_prev]
        except IndexError:
            prev_event = past_events_ids[-1]

        return next_event, prev_event




class UpcomingMatches(BaseModel):
    __tablename__ = 'upcoming_matches'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    card = Column(String())
    first_competitor = Column(String())
    first_competitor_wins_loses = Column(String())
    second_competitor = Column(String())
    second_competitor_wins_loses = Column(String())
    match_number = Column(Integer())
    odds = Column(String())
    event_title = Column(String(), ForeignKey(column=Events.event_title,
                                              onupdate='CASCADE',
                                              ondelete='SET NULL'))

    def __str__(self):
        # Check for odds
        odds = self.odds or ""
        # Try to get link for competitors
        # fighter_first_competitor:Fighters = await Fighters.get_fighter_by_name(self.first_competitor.__str__())
        # if fighter_first_competitor:
        #     first_competitor = f"<a href='{fighter_first_competitor.link}'>{self.first_competitor}</a>"
        # else:
        #     first_competitor = f"{self.first_competitor}"
        #
        # fighter_second_competitor: Fighters = await Fighters.get_fighter_by_name(self.second_competitor.__str__())
        # if fighter_second_competitor:
        #     second_competitor = f"<a href='{fighter_second_competitor.link}'>{self.second_competitor}</a>"
        # else:
        #     second_competitor = f"{self.second_competitor}"

        text = f"{self.match_number}.{self.first_competitor}({self.first_competitor_wins_loses}) vs. " \
               f"{self.second_competitor}({self.second_competitor_wins_loses}) " \
               f"<code>{odds}</code>"

        return text
    @classmethod
    async def get_matches_for_event(cls, event:Events):
        matches = await UpcomingMatches.query.where(UpcomingMatches.event_title == event.event_title).gino.all()
        return matches

class PastMatches(BaseModel):
    __tablename__ = 'past_matches'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    card = Column(String())
    first_competitor = Column(String())
    first_competitor_wins_loses = Column(String())
    second_competitor = Column(String())
    second_competitor_wins_loses = Column(String())
    winner = Column(Integer()) # 1 if first, 2 if second, 0 if draw
    match_result = Column(String())
    match_result_how = Column(String())
    match_result_when = Column(String())
    event_title = Column(String(), ForeignKey(column=Events.event_title,
                                              onupdate='CASCADE',
                                              ondelete='SET NULL'))

    def __str__(self):
        text = str()
        if self.winner == 1:
            text = f"🏅<b>{self.first_competitor}</b>({self.first_competitor_wins_loses}) vs. " \
                   f"{self.second_competitor}({self.second_competitor_wins_loses})\n" \
                   f"<i>{self.match_result}, {self.match_result_how}, {self.match_result_when}</i>"
        elif self.winner == 2:
            text = f"{self.first_competitor}({self.first_competitor_wins_loses}) vs. " \
                   f"🏅<b>{self.second_competitor}({self.second_competitor_wins_loses})</b>\n" \
                   f"<i>{self.match_result}, {self.match_result_how}, {self.match_result_when}</i>"
        else:
            text = f"{self.first_competitor}({self.first_competitor_wins_loses}) vs. " \
                   f"{self.second_competitor}({self.second_competitor_wins_loses})\n" \
                   f"<i>{self.match_result}, {self.match_result_when}</i>"

        return text



    @classmethod
    async def get_matches_for_event(cls, event:Events):
        matches = await PastMatches.query.where(PastMatches.event_title == event.event_title).gino.all()

        return matches

