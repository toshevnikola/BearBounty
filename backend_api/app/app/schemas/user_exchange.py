from typing import Optional, List

from pydantic import BaseModel, EmailStr

# Shared properties
from app.schemas import Exchange


class UserExchangeBase(BaseModel):
    exchange_id: int = None


# Properties to receive via API on creation
class UserExchangeCreate(UserExchangeBase):
    exchange_id: int
    api_key: str
    api_secret: str


# Properties to receive via API on update
class UserExchangeUpdate(UserExchangeBase):
    api_key: Optional[str]
    api_secret: Optional[str]


class UserExchangeInDBBase(UserExchangeBase):
    id: Optional[int] = None
    user_id: int = None
    is_valid: Optional[bool] = False
    balance: Optional[float] = None

    class Config:
        orm_mode = True


class UserExchangeInDB(UserExchangeInDBBase):
    api_key: Optional[str] = None
    api_secret: Optional[str] = None


# Additional properties to return via API
class UserExchange(UserExchangeInDBBase):
    exchange: Exchange
