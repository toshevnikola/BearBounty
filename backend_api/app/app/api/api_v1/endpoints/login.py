from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from schemas import User
from schemas.user import UserLogin

router = APIRouter()


@router.post('/login')
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if user.email != "test@example.com" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=user.email)
    return {"access_token": access_token}
