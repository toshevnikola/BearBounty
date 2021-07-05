from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .strategy import Strategy  # noqa: F401


class Bot(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="bots")
    account_id = Column(Integer, ForeignKey("account.id"))
    account = relationship("Account", back_populates="bots")
    strategy_id = Column(Integer, ForeignKey('strategy.id'))
    strategy = relationship("Strategy", back_populates="bots")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    profit_24h = Column(Numeric, default=0.0, nullable=True)
    profit_all_time = Column(Numeric, default=0.0, nullable=True)
    is_running = Column(Boolean, default=False, nullable=True)
