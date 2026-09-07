from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_learning_project.db.models import Users
from src.fastapi_learning_project.repositories.base import BaseRepository


class UserRepository(BaseRepository[Users]):
    """
    user repository for performing database operations related to the Users model.
    """
    
    def __init__(self, session: AsyncSession):
        # مدل Users را به کلاس پایه می‌دهیم
        super().__init__(model=Users, session=session)

    async def get_by_email(self, email: str) -> Users | None:
        """
        access a user by their email. This method ensures that users can only access their own data, preventing BOLA vulnerabilities.
        """
        statement = select(Users).where(Users.email == email)
        
        result = await self.session.execute(statement)
        return result.scalars().one_or_none()