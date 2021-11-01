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
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.dca_bot import DCABot  # noqa


class Deal(Base):
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey(DCABot.id), index=True)
    pair = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    bot = relationship("DCABot", back_populates="deals")
    # user_exchange = relationship("UserExchange", back_populates="exchange")
    orders = relationship("Order", back_populates="deal")
