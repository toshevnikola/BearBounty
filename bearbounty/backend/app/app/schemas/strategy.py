from typing import Optional

from pydantic import BaseModel


# Shared properties
class StrategyBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class StrategyCreate(StrategyBase):
    name: str



# Properties to receive on item update
class StrategyUpdate(StrategyBase):
    pass


# Properties shared by models stored in DB
class StrategyInDBBase(StrategyBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Strategy(StrategyInDBBase):
    pass


# Properties properties stored in DB
class StrategyInDB(StrategyInDBBase):
    pass
