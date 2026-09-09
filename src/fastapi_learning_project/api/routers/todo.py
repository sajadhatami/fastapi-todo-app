from typing import Annotated
from fastapi import APIRouter, Depends, status

from fastapi_learning_project.api.dependencies import get_current_user, get_todo_service
from fastapi_learning_project.db.models import Users
from fastapi_learning_project.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from fastapi_learning_project.services.todo import TodoService

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]
CurrentUserDep = Annotated[Users, Depends(get_current_user)]


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user: CurrentUserDep,
    service: TodoServiceDep,
):
    """Create a new Todo scoped to the authenticated user."""
    return await service.create_todo(user_id=current_user.id, todo_data=todo_data)


@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    current_user: CurrentUserDep,
    service: TodoServiceDep,
):
    """Get all Todos for the authenticated user."""
    return await service.get_user_todos(user_id=current_user.id)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    current_user: CurrentUserDep,
    service: TodoServiceDep,
):
    """Get a specific Todo by its ID securely."""
    return await service.get_todo_by_id(todo_id=todo_id, user_id=current_user.id)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: CurrentUserDep,
    service: TodoServiceDep,
):
    """Update an existing Todo securely."""
    return await service.update_todo(
        todo_id=todo_id,
        user_id=current_user.id,
        update_data=todo_data,
    )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user: CurrentUserDep,
    service: TodoServiceDep,
):
    """Delete a Todo securely."""
    await service.delete_todo(todo_id=todo_id, user_id=current_user.id)