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
    division = Column(String())
    rank = Column(String())
    image = Column(String())
    nickname = Column(String())
    wins_loses = Column(String())
    stats = Column(JSONB())
    last_fight_event = Column(String())
    last_fight_date = Column(String())
    last_fight_headline = Column(String())
