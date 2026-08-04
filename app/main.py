from fastapi import FastAPI
import logging

from app.api.v1.summary import router as summary_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


app = FastAPI()

app.include_router(summary_router)

@app.get("/")
def home():
    return {"message": "Hello, Roshan! My first FastAPI app is running."}

@app.get("/student")
def student():
    return {
        "name": "Roshan",
        "course": "B.Tech CSE"
    }


@app.get("/city")
def city():
    return {
        "city": "Delhi"
    }
