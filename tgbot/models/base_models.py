from typing import List

from gino import Gino
import sqlalchemy as sa
from sqlalchemy import Column, DateTime

db = Gino()

class BaseModel(db.Model):
    class BaseModel(db.Model):
        __abstract__ = True

        def __str__(self):
            model = self.__class__.__name__
            table: sa.Table = sa.inspect(self.__class__)
            primary_key_columns: List[sa.Column] = table.columns
            values = {
                column.name: getattr(self, self._column_name_map[column.name])
                for column in primary_key_columns
            }
            values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
            return f"<{model} {values_str}>"

    class TimeBaseModel(BaseModel):
        __abstract__ = True

        created_at = Column(DateTime(timezone=True), server_default=db.func.now())
        updated_at = Column(DateTime(timezone=True),
                            default=db.func.now(),
                            onupdate=db.func.now(),
                            server_default=db.func.now())
