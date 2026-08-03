from fastapi import FastAPI

app = FastAPI()

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

from app.models.request_models import SummaryRequest

from app.services.summarizer import generate_summary

@app.post("/summarize")
def summarize(request: SummaryRequest):
    summary = generate_summary(request.text)

    return {
    "summary": summary
}