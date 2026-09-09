from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning_project.db.models import Todos


class TodoRepository:
    """Domain-specific repository for handling Todos persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, todo: Todos) -> Todos:
        """Add a new Todo instance to the session."""
        self.session.add(todo)
        # Flush sends the SQL INSERT to the database to populate the generated fields (like ID),
        # but does NOT commit the transaction.
        await self.session.flush()
        return todo

    async def get_by_id_and_user_id(self, todo_id: int, user_id: int) -> Todos | None:
        """Fetch a single todo scoped to a specific user to prevent BOLA vulnerabilities."""
        stmt = (
            select(Todos)
            .where(Todos.id == todo_id)
            .where(Todos.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: int) -> Sequence[Todos]:
        """Fetch all todos belonging to a specific user."""
        stmt = select(Todos).where(Todos.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, todo: Todos) -> None:
        """Mark a Todo instance for deletion."""
        await self.session.delete(todo)
        await self.session.flush()