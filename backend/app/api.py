import fastapi as fa

app = fa.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}