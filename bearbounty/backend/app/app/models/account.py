from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="accounts")
    bots = relationship("Bot", back_populates="account")
    connected_at = Column(DateTime, default=datetime.now)
    connection_updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    total_balance = Column(Numeric)
    available_balance = Column(Numeric)
    reserved_balance = Column(Numeric)
    is_valid = Column(Boolean, default=False)
