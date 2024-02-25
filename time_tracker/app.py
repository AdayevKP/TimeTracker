import fastapi as fa
from fastapi.middleware import cors

from time_tracker.api.routers import projects, stats, time_entries


app = fa.FastAPI()
app.include_router(projects.router)
app.include_router(time_entries.router)
app.include_router(stats.router)


origins = [
    "http://localhost",
    "http://localhost:5173",  # local dev frontend
]

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(fa.exceptions.RequestValidationError)
async def validation_exception_handler(
    request: fa.Request, exc: fa.exceptions.RequestValidationError
) -> fa.Response:
    return fa.responses.PlainTextResponse(str(exc), status_code=400)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello Time Tracker!"}
