import fastapi as fa

from time_tracker.api.routers import projects, time_entries

app = fa.FastAPI()
app.include_router(projects.router)
app.include_router(time_entries.router)


@app.exception_handler(fa.exceptions.RequestValidationError)
async def validation_exception_handler(request, exc):
    return fa.responses.PlainTextResponse(str(exc), status_code=400)


@app.get("/")
async def root():
    return {"message": "Hello Time Tracker!"}
