from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_learning_project.db.models import Users


class UserRepository:
    """Domain-specific repository for handling Users persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, user: Users) -> Users:
        """Add a new User instance to the database session."""
        self.session.add(user)
        # Flush sends the SQL INSERT command to generate the ID, but keeps the transaction open.
        await self.session.flush()
        return user

    async def get_by_email(self, email: str) -> Users | None:
        """Fetch a user by their unique email address (typically used for login)."""
        stmt = select(Users).where(Users.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_id(self, user_id: int) -> Users | None:
        """Fetch a user by their primary key ID."""
        stmt = select(Users).where(Users.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, user: Users) -> None:
        """Mark a User instance for deletion."""
        await self.session.delete(user)
        await self.session.flush()