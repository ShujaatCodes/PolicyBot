import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base, get_db
from app.models import User, UserRole
from app.auth.service import hash_password


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db(engine):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        # Clean tables before each test
        from sqlalchemy import text
        await session.execute(text("DELETE FROM users"))
        await session.execute(text("DELETE FROM policy_documents"))
        await session.commit()
        yield session


@pytest_asyncio.fixture
async def client(db):
    from app.main import app
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_user(db):
    user = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=hash_password("adminpass123"),
        role=UserRole.admin,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def employee_user(db):
    user = User(
        name="Employee User",
        email="employee@example.com",
        hashed_password=hash_password("emppass123"),
        role=UserRole.employee,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
