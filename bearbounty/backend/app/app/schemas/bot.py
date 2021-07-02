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
    pass


# Properties shared by models stored in DB
class BotInDBBase(BotBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Bot(BotInDBBase):
    pass


# Properties properties stored in DB
class BotInDB(BotInDBBase):
    pass
