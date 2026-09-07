from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_learning_project.db.models import Todos
from src.fastapi_learning_project.repositories.base import BaseRepository

class TodoRepository(BaseRepository[Todos]):
    """
    Repository class for managing Todos. 
    """
    
    def __init__(self, session: AsyncSession):
        super().__init__(model=Todos, session=session)

    async def get_all_by_user_id(self, user_id: int) -> list[Todos]:
        """
        access all todos for a specific user. This method ensures that users can only access their own todos, preventing BOLA vulnerabilities.
        """
        statement = select(Todos).where(Todos.user_id == user_id)
        
        # اجرای دستور و گرفتن نتیجه
        result = await self.session.execute(statement)
        
        # تبدیل نتیجه به یک لیست از آبجکت‌های ORM
        return list(result.scalars().all())

    async def get_by_id_and_user_id(self, todo_id: int, user_id: int) -> Todos | None:
        """
        access a specific todo, but only if it belongs to the same user.
        This method ensures that users can only access their own todos, preventing BOLA vulnerabilities.
        """
        statement = (
            select(Todos)
            .where(Todos.id == todo_id)
            .where(Todos.user_id == user_id)
        )
        
        result = await self.session.execute(statement)
        
        # اگر تسک وجود داشت و متعلق به کاربر بود، آن را برمی‌گرداند.
        # اگر وجود نداشت، یا متعلق به کاربر دیگری بود، None برمی‌گرداند.
        return result.scalars().one_or_none()