import fastapi as fa

from app.api.routers import projects, time_entries
# from app.db import models, database

app = fa.FastAPI()
app.include_router(projects.router)
app.include_router(time_entries.router)


# models.Base.metadata.create_all(bind=database.async_engine)


@app.exception_handler(fa.exceptions.RequestValidationError)
async def validation_exception_handler(request, exc):
    return fa.responses.PlainTextResponse(str(exc), status_code=400)


@app.get("/")
async def root():
    return {"message": "Hello Time Tracker!"}
