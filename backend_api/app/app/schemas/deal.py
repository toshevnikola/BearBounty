from __future__ import annotations
from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, EmailStr

# Shared properties


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
    bot: Optional[Any]
    orders: Optional[list]


Deal.update_forward_refs()
