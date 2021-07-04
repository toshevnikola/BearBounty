import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class BotBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    strategy_id: int


# Properties to receive on bot creation
class BotCreate(BotBase):
    name: str


# Properties to receive on bot update
class BotUpdate(BotBase):
    is_running: Optional[bool] = False


# Properties shared by models stored in DB
class BotInDBBase(BotBase):
    id: int
    name: str
    owner_id: int
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    profit_24h: Optional[float] = 0.00
    profit_all_time: Optional[float] = 0.00
    is_running:Optional[bool] = False

    class Config:
        orm_mode = True


# Properties to return to client
class Bot(BotInDBBase):
    pass


# Properties stored in DB
class BotInDB(BotInDBBase):
    pass
