from fastapi import APIRouter
from app.api.api_v1.endpoints import login, user

api_router = APIRouter()
api_router.include_router(router=login.router, tags=['login'])
api_router.include_router(router=user.router, tags=['user'])
