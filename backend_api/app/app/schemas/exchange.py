from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class ExchangeBase(BaseModel):
    name: Optional[str] = None
    supported_pairs: List[str] = []


# Properties to receive via API on creation
class ExchangeCreate(ExchangeBase):
    name: str
    supported_pairs: List[str]


# Properties to receive via API on update
class ExchangeUpdate(ExchangeBase):
    supported_pairs: List[str]
    is_available: Optional[bool]


class ExchangeInDBBase(ExchangeBase):
    id: Optional[int] = None
    is_available: Optional[bool] = True

    class Config:
        orm_mode = True


class ExchangeInDB(ExchangeInDBBase):
    pass


# Additional properties to return via API
class Exchange(ExchangeInDBBase):
    pass
