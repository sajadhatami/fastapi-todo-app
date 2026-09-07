from typing import Any 
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.fastapi_learning_project.db.base import Base


class BaseRepository[ModelType: Base]:
    """
    base class for data access layer, providing common CRUD operations for SQLAlchemy models.
    """
    def __init__(self, model: type[ModelType] ,session: AsyncSession):
        self.model = model
        self.session = session
    
    async def add(self, instance: ModelType):
        """
        Add a new instance to the database.
        """
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def get_by_id(self, id: Any) -> ModelType | None:
        """
        Get an instance by its ID.
        """
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.execute(statement)
        return result.scalars().one_or_none()