from fastapi import FastAPI

from users import router as users_router

app = FastAPI()

app.include_router(users_router.router)


@app.get("/")
def test():
    return {"message": "hello"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
