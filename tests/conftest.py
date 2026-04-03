"""Configuração do pytest: banco SQLite em memória, cliente de teste."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
import main

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client(reset_db):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    with TestClient(main.app) as c:
        yield c
    main.app.dependency_overrides.clear()


@pytest.fixture()
def admin_token(client):
    client.post("/auth/register", json={"username": "admin_test", "password": "admin123", "role": "admin"})
    r = client.post("/auth/token", data={"username": "admin_test", "password": "admin123"})
    return r.json()["access_token"]


@pytest.fixture()
def user_token(client):
    client.post("/auth/register", json={"username": "user_test", "password": "user123", "role": "user"})
    r = client.post("/auth/token", data={"username": "user_test", "password": "user123"})
    return r.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}
