from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, NoPasswordUserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_without_pass(self, db: Session, obj_in: NoPasswordUserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            provider=obj_in.provider,
            provider_id=obj_in.provider_id,
            is_superuser=obj_in.is_superuser,
            first_name=obj_in.first_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        db_user = self.get_by_email(db, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    def retrieve_user(
            self, db: Session, provider: str, provider_user_id: str
    ) -> Optional[User]:
        db_user = (
            db.query(User).filter(User.provider == provider, User.provider_id == provider_user_id).first()
        )
        return db_user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
