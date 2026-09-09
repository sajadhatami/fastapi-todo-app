from fastapi_learning_project.repositories.uow import UnitOfWork
from fastapi_learning_project.services.todo import TodoService




def get_todo_service() -> TodoService:
    """
    Dependency provider for TodoService.
    Instantiates the UnitOfWork and injects it into the service.
    This allows FastAPI to provide a ready-to-use service to our routes automatically.
    """
    uow = UnitOfWork()
    return TodoService(uow=uow)