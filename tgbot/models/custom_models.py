from sqlalchemy import Column, String, DateTime, Text, sql

from tgbot.models.base_models import BaseModel


class News(BaseModel):
    __tablename__ = 'news'
    title = Column(String(), primary_key=True)
    category = Column(String())
    link = Column(String())
    pubDate= Column(DateTime(timezone=True))
    description = Column(Text())
    image = Column(String())

    query: sql.Select