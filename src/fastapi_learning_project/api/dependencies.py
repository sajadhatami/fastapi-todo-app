from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi_learning_project.core.security import decode_access_token
from fastapi_learning_project.db.models import Users
from fastapi_learning_project.repositories.uow import UnitOfWork
from fastapi_learning_project.services.auth import AuthService
from fastapi_learning_project.services.exceptions import InvalidCredentialsException
from fastapi_learning_project.services.todo import TodoService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_todo_service() -> TodoService:
    """Dependency provider for TodoService."""
    uow = UnitOfWork()
    return TodoService(uow=uow)


def get_auth_service() -> AuthService:
    """Dependency provider for AuthService."""
    uow = UnitOfWork()
    return AuthService(uow=uow)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Users:
    """
    Decodes Bearer token and validates user identity via AuthService.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception

    try:
        return await auth_service.get_user_by_id(user_id)
    except InvalidCredentialsException:
        raise credentials_exception