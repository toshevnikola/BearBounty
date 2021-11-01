from datetime import timedelta

import pydantic
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

import app.crud as crud
from app.api import deps
from app.core.config import settings
from app.core.security import denylist
from app.schemas.token import JWTTokenResponse
from app.schemas.user import UserLogin, User, NoPasswordUserCreate
from google.oauth2 import id_token
from google.auth.transport import requests
from schemas.token import Token

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


@router.post("/google-login", response_model=JWTTokenResponse)
async def google_login(
        token: Token, db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends()
):
    info = id_token.verify_oauth2_token(
        token.token, requests.Request(), settings.GOOGLE_CLIENT_ID
    )
    user_id = info.get("sub", None)
    email = info.get('email', None)
    first_name = info.get('given_name', None)
    user = crud.user.retrieve_user(db, provider="google", provider_user_id=user_id)
    if not user:
        obj_in = NoPasswordUserCreate(email=email, provider="google", provider_id=user_id, first_name=first_name,
                                      )
        user = crud.user.create_without_pass(db, obj_in=obj_in)

    access_token = Authorize.create_access_token(
        subject=user.id, expires_time=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.id, expires_time=settings.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    return JWTTokenResponse(access_token=access_token, refresh_token=refresh_token)


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
