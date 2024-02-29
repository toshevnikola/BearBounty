from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from requests import Session

from utils import get_current_user

from backend_api.app.app.core.config import settings

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_top_100_cryptocurrencies(*, Authorize: AuthJWT = Depends()):
    current_user = get_current_user(Authorize)
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {"start": "1", "limit": "100", "convert": "USD"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": settings.COINMARKETCAP_KEY,
        }

        session = Session()
        session.headers.update(headers)
        res = session.get(url, params=parameters)
        if res.status_code == 200:
            return res.json()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=res.text
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Coingecko unavailable:{str(e)}",
        )
