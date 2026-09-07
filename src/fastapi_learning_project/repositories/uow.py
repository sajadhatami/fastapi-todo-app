from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_learning_project.db.session import AsyncSessionLocal
from src.fastapi_learning_project.repositories.todo import TodoRepository
from src.fastapi_learning_project.repositories.user import UserRepository


class UnitOfWork:
    """
    Coordinates transactions and shares a single database session 
    across all domain repositories.
    """

    def __init__(self) -> None:
        self.session_factory = AsyncSessionLocal
        self._session: AsyncSession | None = None
        self.todos: TodoRepository | None = None
        self.users: UserRepository | None = None

    async def __aenter__(self) -> "UnitOfWork":
        """
        Invoked when entering the 'async with' block.
        Opens a session and initializes repositories with this shared session.
        """
        self._session = self.session_factory()
        
        # Inject the SAME session into all repositories
        self.todos = TodoRepository(self._session)
        self.users = UserRepository(self._session)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Invoked when exiting the 'async with' block.
        Handles commit on success, rollback on exception, and safe cleanup.
        """
        if self._session is None:
            return

        try:
            if exc_type is not None:
                # An exception occurred, rollback the transaction
                await self._session.rollback()
            else:
                # No exception, commit the changes
                await self._session.commit()
        finally:
            # Always close the session to return the connection to the pool
            await self._session.close()