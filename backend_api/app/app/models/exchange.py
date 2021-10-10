import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Exchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    supported_pairs = Column(ARRAY(String))
    is_available = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    user_exchange = relationship("UserExchange", back_populates="exchange")
