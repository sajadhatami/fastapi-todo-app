# src/fastapi_learning_project/api/routers/todo.py

from typing import Annotated
from fastapi import APIRouter, Depends, status

from fastapi_learning_project.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from fastapi_learning_project.services.todo import TodoService
from fastapi_learning_project.api.dependencies import get_todo_service

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]

CURRENT_USER_ID = 1

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    service: TodoServiceDep 
):
    """Create a new Todo."""
    return await service.create_todo(user_id=CURRENT_USER_ID, todo_data=todo_data)

@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    service: TodoServiceDep
):
    """Get all Todos for the current user."""
    return await service.get_user_todos(user_id=CURRENT_USER_ID)

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    service: TodoServiceDep
):
    """Get a specific Todo by its ID securely."""
    return await service.get_todo_by_id(todo_id=todo_id, user_id=CURRENT_USER_ID)

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    service: TodoServiceDep
):
    """Update an existing Todo securely."""
    return await service.update_todo(todo_id=todo_id, user_id=CURRENT_USER_ID, update_data=todo_data)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    service: TodoServiceDep
):
    """Delete a Todo securely."""
    await service.delete_todo(todo_id=todo_id, user_id=CURRENT_USER_ID)