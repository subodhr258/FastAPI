from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserOut
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from alembic import command

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine) #clear out previous tables
    Base.metadata.create_all(bind=engine) #build our new tables and keep it so you can see it after the test too.
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session): #session fixture is a requirement for the client fixture.
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    #run our code before our test
    # Base.metadata.drop_all(bind=engine) #clear out previous tables
    # Base.metadata.create_all(bind=engine) #build our new tables and keep it so you can see it after the test too.
    # command.upgrade("head") #with alembic
    yield TestClient(app)
    # command.downgrade("base") #with alembic
    #run our code after the test finishes
    #not deleting all if you wanna poke around and take a look.
