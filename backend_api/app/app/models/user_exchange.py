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
from app.models.exchange import Exchange  # noqa
from app.models.user import User  # noqa


class UserExchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    api_secret = Column(String)
    balance = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    exchange_id = Column(Integer, ForeignKey(Exchange.id), index=True)
    exchange = relationship("Exchange", back_populates="user_exchange")
    is_valid = Column(Boolean)
