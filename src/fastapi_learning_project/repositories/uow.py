from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_learning_project.db.session import AsyncSessionLocal
from src.fastapi_learning_project.repositories.todo import TodoRepository
from src.fastapi_learning_project.repositories.user import UserRepository


class UnitOfWork:
    """
    this class implements the Unit of Work pattern for managing database transactions and repositories.
    """

    def __init__(self) -> None:
        # initialize the session and repositories to None. They will be set when entering the context manager.
        self._session: AsyncSession | None = None
        self._todos: TodoRepository | None = None
        self._users: UserRepository | None = None

    async def __aenter__(self) -> "UnitOfWork":
        """
        async context manager entry method. It initializes the database session and repositories.
        """
        # ساخت یک Session جدید از کارخانه Session
        self._session = AsyncSessionLocal()
        
        # ساخت Repositoryها و دادن Session مشترک به آن‌ها
        self._todos = TodoRepository(session=self._session)
        self._users = UserRepository(session=self._session)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        async context manager exit method. It handles committing or rolling back the transaction based on whether an exception occurred.
        """
        if self._session is None:
            return

        try:
            if exc_type is not None:
                # اگر خطایی (Exception) در طول عملیات رخ داده باشد
                await self._session.rollback()
            else:
                # اگر هیچ خطایی رخ نداده باشد
                await self._session.commit()
        finally:
            # در هر حالت (موفقیت یا شکست)، Session را می‌بندیم 
            # تا اتصال به دیتابیس آزاد شود و Connection Leak نداشته باشیم
            await self._session.close()
            self._session = None

    # --- Propertyها برای دسترسی ایمن به Repositoryها ---
    
    @property
    def todos(self) -> TodoRepository:
        if self._todos is None:
            raise RuntimeError("Unit of Work is not initialized. Use 'async with UnitOfWork()'.")
        return self._todos

    @property
    def users(self) -> UserRepository:
        if self._users is None:
            raise RuntimeError("Unit of Work is not initialized. Use 'async with UnitOfWork()'.")
        return self._users