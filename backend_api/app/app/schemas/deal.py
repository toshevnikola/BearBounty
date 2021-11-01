from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

# Shared properties
from app.schemas import DCABot


class DealBase(BaseModel):
    bot_id: int
    pair: Optional[str]
    is_active: Optional[bool]
    orders: Optional[list]


# Properties to receive via API on creation
class DealCreate(DealBase):
    is_active: Optional[bool] = True


# Properties to receive via API on update
class DealUpdate(DealBase):
    pass


class DealInDBBase(DealBase):
    class Config:
        orm_mode = True


class DealInDB(DealInDBBase):
    pass


# Additional properties to return via API
class Deal(DealInDBBase):
    created_at: datetime
    updated_at: datetime
    bot: DCABot
