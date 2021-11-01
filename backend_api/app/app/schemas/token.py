from pydantic import BaseModel


class Token(BaseModel):
    token: str


class JWTTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
