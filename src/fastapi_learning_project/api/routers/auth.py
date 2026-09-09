from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_learning_project.api.dependencies import get_auth_service
from fastapi_learning_project.schemas.user import TokenResponse, UserCreate, UserResponse
from fastapi_learning_project.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    user_data: UserCreate,
    service: AuthServiceDep,
):
    """Registers a new user account."""
    return await service.register(user_data=user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain JWT access token"
)
async def login(
    form_data: OAuth2FormDep,
    service: AuthServiceDep,
):
    """
    Authenticates credentials and returns a Bearer access token.
    FastAPI OAuth2 standard maps the user's email into form_data.username.
    """
    token = await service.login(
        email=form_data.username,
        password=form_data.password
    )
    return TokenResponse(access_token=token)