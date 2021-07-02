from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Bot])
def read_bots(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bots.
    """
    if crud.user.is_superuser(current_user):
        bots = crud.bot.get_multi(db, skip=skip, limit=limit)
    else:
        bots = crud.bot.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return bots


@router.post("/", response_model=schemas.Bot)
def create_bot(
    *,
    db: Session = Depends(deps.get_db),
    bot_in: schemas.BotCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bot.
    """
    bot = crud.bot.create_with_owner(db=db, obj_in=bot_in, owner_id=current_user.id)
    return bot


@router.put("/{id}", response_model=schemas.Bot)
def update_bot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    bot_in: schemas.BotUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a bot.
    """
    bot = crud.bot.get(db=db, id=id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if not crud.user.is_superuser(current_user) and (bot.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bot = crud.bot.update(db=db, db_obj=bot, obj_in=bot_in)
    return bot


@router.get("/{id}", response_model=schemas.Bot)
def read_bot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get bot by ID.
    """
    bot = crud.bot.get(db=db, id=id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if not crud.user.is_superuser(current_user) and (bot.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bot


@router.delete("/{id}", response_model=schemas.Bot)
def delete_bot(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a bot.
    """
    bot = crud.bot.get(db=db, id=id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if not crud.user.is_superuser(current_user) and (bot.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bot = crud.bot.remove(db=db, id=id)
    return bot
