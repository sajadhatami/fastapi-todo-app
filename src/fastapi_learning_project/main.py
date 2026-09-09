from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference
from fastapi_learning_project.services.exceptions import BaseDomainException, TodoNotFoundException


from fastapi_learning_project.api.routers.todo import router as todo_router


app = FastAPI()

@app.exception_handler(TodoNotFoundException)
async def todo_not_found_exception_handler(request: Request, exc: TodoNotFoundException):
    """
    Catches TodoNotFoundException globally and returns a clean 404 HTTP response.
    """
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )

@app.exception_handler(BaseDomainException)
async def domain_exception_handler(request: Request, exc: BaseDomainException):
    """
    Catches any other generic domain exceptions and returns a 400 Bad Request.
    """
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )







# --- Include Routers ---
app.include_router(todo_router)









@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
###
@app.get("/")
def root():
    return {"message": "Hello World"}



