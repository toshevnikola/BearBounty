from fastapi import APIRouter
from app.api.api_v1.endpoints import login, user, exchange, user_exchange

api_router = APIRouter()
api_router.include_router(prefix='/login', router=login.router, tags=['login'])
api_router.include_router(prefix='/users', router=user.router, tags=['user'])
api_router.include_router(prefix='/exchanges', router=exchange.router, tags=['exchange'])
api_router.include_router(prefix='/user_exchanges', router=user_exchange.router, tags=['user_exchange'])
