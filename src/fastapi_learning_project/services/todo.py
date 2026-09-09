from fastapi_learning_project.repositories.uow import UnitOfWork
from fastapi_learning_project.db.models import Todos
from fastapi_learning_project.schemas.todo import TodoCreate
from fastapi_learning_project.services.exceptions import TodoNotFoundException
from collections.abc import Sequence
from fastapi_learning_project.schemas.todo import TodoUpdate

class TodoService:
    """
    Service layer for managing Todo business logic.
    It isolates business rules from the web/API layer.
    """

    def __init__(self, uow: UnitOfWork) -> None:
        """
        Injecting Unit of Work to handle database transactions safely
        """
        self.uow = uow
        
    async def create_todo(self, user_id: int, todo_data: TodoCreate) -> Todos:
        """
        Creates a new todo for a specific user.
        'async with self.uow' starts a safe database transaction.
        If an error happens inside this block, the database automatically rolls back.
        """
        async with self.uow:
            # 1. Convert the Pydantic schema (todo_data) into a normal Python dictionary
            data_dict = todo_data.model_dump()
            
            # 2. Create the SQLAlchemy database model
            # We explicitly pass the user_id to link the todo to its owner
            new_todo = Todos(**data_dict, user_id=user_id)
            
            # 3. Use the repository to insert the model into the database session
            added_todo = await self.uow.todos.add(new_todo)
            
            # 4. We do not explicitly call commit() here because the UnitOfWork
            # automatically commits when exiting the 'async with' block successfully!
            
            return added_todo
    
    async def get_user_todos(self, user_id: int) -> Sequence[Todos]:
        """
        Fetches all todos that belong to a specific user.
        We strictly filter by user_id to ensure users only see their own data.
        """
        async with self.uow:
            # We call the repository method that already filters by user_id
            todos = await self.uow.todos.get_all_by_user_id(user_id=user_id)
            return todos

    async def get_todo_by_id(self, todo_id: int, user_id: int) -> Todos:
        """
        Fetches a single todo by its ID, BUT ensures it belongs to the user.
        If the todo does not exist or belongs to someone else, we raise an exception.
        """
        async with self.uow:
            # The repository method checks BOTH todo_id and user_id (Preventing BOLA attacks)
            todo = await self.uow.todos.get_by_id_and_user_id(todo_id=todo_id, user_id=user_id)
            
            if not todo:
                # We raise our custom domain exception instead of an HTTPException
                raise TodoNotFoundException(f"Todo with ID {todo_id} not found or access denied.")
            
            return todo
    
    async def update_todo(self, todo_id: int, user_id: int, update_data: TodoUpdate) -> Todos:
        """
        Updates an existing todo safely.
        Uses 'exclude_unset=True' to only update fields provided by the user.
        """
        async with self.uow:
            # 1. Fetch securely
            todo = await self.uow.todos.get_by_id_and_user_id(todo_id=todo_id, user_id=user_id)
            if not todo:
                raise TodoNotFoundException(f"Todo with ID {todo_id} not found.")

            # 2. Update fields dynamically
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(todo, key, value) 

            # 3. Transaction commits automatically when exiting 'async with'
            return todo

    async def delete_todo(self, todo_id: int, user_id: int) -> None:
        """
        Deletes a todo securely.
        """
        async with self.uow:
            todo = await self.uow.todos.get_by_id_and_user_id(todo_id=todo_id, user_id=user_id)
            if not todo:
                raise TodoNotFoundException(f"Todo with ID {todo_id} not found.")

            await self.uow.todos.delete(todo)