import asyncio
from sqlalchemy import text
from src.fastapi_learning_project.db.session import AsyncSessionLocal
from src.fastapi_learning_project.core.config import settings

# Print the database URL to verify it's correct
print("🔍 DATABASE_URL =", settings.DATABASE_URL)

async def test_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        print(f"Result: {result.scalar()}")

asyncio.run(test_connection())