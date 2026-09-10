import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker

from fastapi_learning_project.main import app
from fastapi_learning_project.db.session import engine
from fastapi_learning_project.repositories.uow import UnitOfWork
from fastapi_learning_project.services.auth import AuthService
from fastapi_learning_project.services.todo import TodoService
from fastapi_learning_project.api.dependencies import get_auth_service, get_todo_service

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture()
async def db_connection():
    """
    Create a database connection for testing.
    """
    async with engine.connect() as conn:
        transaction = await conn.begin()
        yield conn
        await transaction.rollback()
    await engine.dispose()

@pytest_asyncio.fixture()
async def client(db_connection):
    """
    make a test client that uses the same database connection and transaction for all requests in a test.
    """
    TestSessionLocal = async_sessionmaker(
        bind=db_connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint"  
    )

    class TestUnitOfWork(UnitOfWork):
        def __init__(self):
            super().__init__()
            self.session_factory = TestSessionLocal

    app.dependency_overrides[get_auth_service] = lambda: AuthService(uow=TestUnitOfWork())
    app.dependency_overrides[get_todo_service] = lambda: TodoService(uow=TestUnitOfWork())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
    app.dependency_overrides.clear()