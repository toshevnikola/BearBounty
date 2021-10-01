from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.crud as crud
from app.api import deps
from app.core.config import settings
from app.core.security import denylist

from app.schemas.user import UserLogin

router = APIRouter()


@router.post("/get-tokens")
async def login(
    user: UserLogin, db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends()
):
    user = crud.user.authenticate(db, email=user.email, password=user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = Authorize.create_access_token(
        subject=user.id, expires_time=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.id, expires_time=settings.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete("/revoke")
def revoke_tokens(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    jti = Authorize.get_raw_jwt()["jti"]
    denylist.add(jti)
    print(denylist)

    return {"detail": "Access token has been revoke"}
