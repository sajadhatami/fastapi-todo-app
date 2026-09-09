from fastapi_learning_project.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from fastapi_learning_project.db.models import Users
from fastapi_learning_project.repositories.uow import UnitOfWork
from fastapi_learning_project.schemas.user import UserCreate
from fastapi_learning_project.services.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
)


class AuthService:
    """Service layer handling user authentication and registration workflows."""

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
    
    
    async def get_user_by_id(self, user_id: int) -> Users:
        """
        Fetches an active user by ID for request authentication context.
        
        Raises:
            InvalidCredentialsException: If user does not exist or is inactive.
        """
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            if user is None or not user.is_active:
                raise InvalidCredentialsException("User not found or inactive.")
            return user

    async def register(self, user_data: UserCreate) -> Users:
        """
        Registers a new user after verifying email uniqueness and hashing the password.
        
        Args:
            user_data: Validated user creation schema.
            
        Returns:
            The created Users ORM model instance.
            
        Raises:
            UserAlreadyExistsException: If the email is already registered.
        """
        async with self.uow:
            # 1. Domain Rule: Email must be unique across the platform
            existing_user = await self.uow.users.get_by_email(email=user_data.email)
            if existing_user:
                raise UserAlreadyExistsException(
                    f"User with email '{user_data.email}' already exists."
                )

            # 2. Extract plain dictionary and hash the raw password using Argon2id
            data_dict = user_data.model_dump()
            raw_password = data_dict.pop("password")
            data_dict["hashed_password"] = hash_password(raw_password)

            # 3. Create ORM instance and persist via repository
            new_user = Users(**data_dict)
            created_user = await self.uow.users.add(new_user)
            
            # UnitOfWork commits the transaction automatically on exiting context
            return created_user

    async def login(self, email: str, password: str) -> str:
        """
        Validates user credentials and issues a signed JWT access token.
        
        Args:
            email: User's registered email address.
            password: Raw plain text password.
            
        Returns:
            Signed JWT access token string.
            
        Raises:
            InvalidCredentialsException: If credentials don't match or user is inactive.
        """
        async with self.uow:
            # 1. Fetch user by email
            user = await self.uow.users.get_by_email(email=email)

            # 2. Prevent User Enumeration: Use constant error messaging
            if not user or not verify_password(password, user.hashed_password):
                raise InvalidCredentialsException("Invalid email or password.")

            # 3. Account status check
            if not user.is_active:
                raise InvalidCredentialsException("Account is deactivated.")

            # 4. Issue token using standard 'sub' (subject) claim
            token_payload = {
                "sub": str(user.id),
                "role": user.role.value,
            }
            access_token = create_access_token(data=token_payload)
        

            return access_token