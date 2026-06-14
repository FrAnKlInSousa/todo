from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from todo.app import app
from todo.database import get_session
from todo.models import User, table_registry
from todo.security import create_password_hash
from todo.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 6, 10)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: AsyncSession):
    password = 'secret123'
    user = User(
        username='user_test',
        email='test@mail.com',
        password=create_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = password
    return user


@pytest.fixture
def token(client, user):
    data = {'username': user.email, 'password': user.clean_password}

    response = client.post('/auth/token', data=data)

    return response.json()['access_token']


@pytest.fixture
def settings():
    settings = Settings()
    # exemplo de manipulação que dá pra fazer com essa fixture
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = 35
    return settings
