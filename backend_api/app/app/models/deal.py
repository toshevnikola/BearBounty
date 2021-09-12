import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    ARRAY,
    Float,
    ForeignKey,
)
from app.db.base_class import Base

from app.models.dca_bot import DCABot  # noqa


class Deal(Base):
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey(DCABot.id), index=True)
    pair = Column(String, nullable=False)
