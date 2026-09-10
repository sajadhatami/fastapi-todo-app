from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware
from fastapi_learning_project.api.routers.auth import router as auth_router
from fastapi_learning_project.api.routers.todo import router as todo_router
from fastapi_learning_project.services.exceptions import (
    BaseDomainException,
    InvalidCredentialsException,
    TodoNotFoundException,
    UserAlreadyExistsException,
)

app = FastAPI(title="FastAPI Todo App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در پروداکشن واقعی فقط دامنه سایت خودتان را وارد کنید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(TodoNotFoundException)
async def todo_not_found_exception_handler(request: Request, exc: TodoNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(BaseDomainException)
async def domain_exception_handler(request: Request, exc: BaseDomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


# --- Include Routers ---
app.include_router(auth_router)
app.include_router(todo_router)


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )


@app.get("/")
def root():
    return {"message": "Hello World"}