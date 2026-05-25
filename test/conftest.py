import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from core.auth.user.user_dto import UserRequest


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        os.environ["DB_CONN"] = postgres.get_connection_url()
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    # os.environ["DB_CONN"] = postgres_container.get_connection_url()
    from database.dbconfig import Base

    engine = create_engine(os.environ["DB_CONN"])
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def default_user(db_session):
    new_user = UserRequest(username="admin", email="admin@example.com",
                           first_name="Admin", last_name="User", phone_number="+447860989076",
                           password="password", confirm_password="password")
    from core.auth.user import user_service
    user = user_service.add_user(new_user, db_session)

    return user

@pytest.fixture()
def get_auth_user(default_user, client, db_session):
    response = client.post("/auth/login",
                           data={
                               "username": default_user.email,
                               "password": "password"})
    data = response.json()
    return {'id': data.get('user').get('id'), 'username': data.get('user').get('username'),
            'email': data.get('user').get('email'), 'role': data.get('user').get('role'),
            'access_token': data.get('access_token')}

@pytest.fixture()
def client(db_session, postgres_container):
    from database.dbconfig import get_db, reset_engine
    reset_engine()
    from main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
