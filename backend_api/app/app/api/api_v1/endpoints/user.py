from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from schemas import User

router = APIRouter()


@router.post(
    "/create", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    if user_in.password != user_in.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and confirm password fields do not match.",
        )
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
def get_current_user(
    Authorize: AuthJWT = Depends(), db: Session = Depends(deps.get_db)
) -> Any:
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    current_user_id = Authorize.get_jwt_subject()
    return crud.user.get(db=db, id=current_user_id)
