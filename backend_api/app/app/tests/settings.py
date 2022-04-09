from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import app
from app.api.deps import get_db
from app.core.config import settings

# engine = create_engine('sqlite://', connect_args={"check_same_thread": False}, poolclass=StaticPool)
engine = create_engine(settings.TEST_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def tests_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = tests_get_db

client = TestClient(app)
