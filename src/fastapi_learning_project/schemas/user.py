from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi_learning_project.db.models import UserRole



class UserBase(BaseModel):
    """
    Base model for user data.
    """
    full_name: str = Field(..., min_length=3, max_length=255, description="The full name of the user.", examples=["sajad hatami"])
    email: EmailStr = Field(..., description="The email address of the user.", examples=["sajadhatamiw@gmail.com"])
    phone_number: str | None = Field(default=None, max_length=11,description="The phone number of the user.", examples=["09190987869"])

class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str = Field(..., min_length=8, max_length=128, description="The password for the user.", examples=["securepassword123"])




class UserResponse(UserBase):
    """
    Model for user response data.
    """
    # configdict allows us to access the attributes of the model directly, making it easier to work with the data.
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    




class UserUpdate(BaseModel):
    """ 
    Model for updating user data.
    """
    full_name: str | None = Field(default=None, min_length=3, max_length=255)
    phone_number: str | None = Field(default=None, max_length=11)
    
    
    
class UserPasswordUpdate(BaseModel):
    """
    Model for updating the user's password.
    """
    current_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)
    
class UserEmailUpdate(BaseModel):
    """
    Model for updating the user's email.
    """
    new_email: EmailStr = Field(..., description="The new email address for the user.", examples=["newemail@gmail.com"])
    current_password: str = Field(..., min_length=8, max_length=128)
