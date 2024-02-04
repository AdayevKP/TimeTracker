from fastapi import FastAPI

from app.api.routers import projects, time_entries

app = FastAPI()
app.include_router(projects.router)
app.include_router(time_entries.router)


@app.get("/")
async def root():
    return {"message": "Hello Time Tracker!"}
