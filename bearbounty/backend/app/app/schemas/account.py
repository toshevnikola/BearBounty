import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class AccountBase(BaseModel):
    name: Optional[str] = None


# Properties to receive on bot creation
class AccountCreate(AccountBase):
    name: str


# Properties to receive on bot update
class AccountUpdate(AccountBase):
    name: Optional[str] = None


# Properties shared by models stored in DB
class AccountInDBBase(AccountBase):
    id: int
    name: str
    owner_id: int
    connected_at: datetime.datetime = None
    connection_updated_at: datetime.datetime = None
    total_balance: Optional[float] = 0.00
    reserved_balance: Optional[float] = 0.00
    available_balance: Optional[float] = 0.00
    is_valid:Optional[bool] = False

    class Config:
        orm_mode = True


# Properties to return to client
class Account(AccountInDBBase):
    pass


# Properties stored in DB
class AccountInDB(AccountInDBBase):
    pass
