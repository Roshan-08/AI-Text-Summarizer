from fastapi import FastAPI
import logging
import time
import uuid

from app.api.v1.summary import router as summary_router
from app.exceptions.handlers import generic_exception_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

@app.middleware("http")
async def log_requests(request, call_next):

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.perf_counter()


    response = await call_next(request)

    process_time = time.perf_counter() - start

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.2f}"

    logger.info(
    f"[{request_id}] "
    f"{request.method} "
    f"{request.url.path} "
    f"{response.status_code} "
    f"{process_time:.2f}s"
)

    return response

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
