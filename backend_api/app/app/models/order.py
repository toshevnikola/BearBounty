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
    Enum,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.deal import Deal  # noqa
from app.constants import OrderStatusEnum, OrderTypeEnum


class Order(Base):
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey(Deal.id), index=True)
    amount = Column(Float, nullable=False)
    fee = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum))
    type = Column(Enum(OrderTypeEnum))
    exchange_order_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    price = Column(Float, nullable=False)
    deal = relationship("Deal", back_populates="orders")
