from fastapi import status, HTTPException


def get_current_user(Authorize) -> int:
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    current_user = Authorize.get_jwt_subject()
    return current_user
