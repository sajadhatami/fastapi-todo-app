from pydantic import BaseModel, ConfigDict, Field
from fastapi_learning_project.db.models import TodoStatus, TodoPriority, TodoType
from datetime import datetime



class TodoBase(BaseModel):
    """ 
    Base model for todo data.
    """
    title: str = Field(..., min_length=1, max_length=255, description="The title of the todo.", examples=["Buy groceries"])
    description: str | None = Field(default=None, max_length=255, description="The description of the todo.", examples=["Buy milk, eggs, and bread"])
    priority: TodoPriority = Field(default=TodoPriority.DEFAULT, description="The priority of the todo.")
    type: TodoType = Field(default=TodoType.TASK, description="The type of the todo.")
    status: TodoStatus = Field(default=TodoStatus.IN_PROGRESS, description="The status of the todo.")
    due_date: datetime | None = Field(default=None, description="The due date of the todo.", examples=["2023-12-31T23:59:59Z"])




class TodoCreate(TodoBase):
    """
    Model for creating a new todo.
    """


class TodoResponse(TodoBase):
    """ 
    Model for todo response data.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(BaseModel):
    """
    Model for updating todo data.
    """
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    priority: TodoPriority | None = Field(default=None)
    type: TodoType | None = Field(default=None)
    status: TodoStatus | None = Field(default=None)
    due_date: datetime | None = Field(default=None)


