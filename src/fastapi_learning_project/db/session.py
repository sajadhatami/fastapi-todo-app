from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi_learning_project.core.config import settings

# 1. creating AsyncEngine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # activate SQL query logging for debugging purposes
    pool_size=10,  # database connection pool size
    max_overflow=20,  # how many connections can be created after the pool reached its size
)

# 2. AsyncSessionMaker 
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 3. یک تابع کمکی برای گرفتن Session (برای استفاده در Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
