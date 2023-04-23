from sqlalchemy import Column, String, DateTime, Text, sql, Integer
from sqlalchemy.dialects.postgresql import JSONB

from tgbot.models.base_models import BaseModel


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

