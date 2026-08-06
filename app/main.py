from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.limiter import limiter
from fastapi import FastAPI
import logging
import time
import uuid


from app.api.v1.summary import router as summary_router
from app.exceptions.handlers import generic_exception_handler
from app.api.v1.health import router as health_router
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Text Summarizer API",
    description="An AI-powered text summarization service built with FastAPI and Google Gemini.",
    version="1.0.0",
    contact={
        "name": "Roshan Kumar",
        "url": "https://github.com/Roshan-08",
    },
)

app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.state.limiter = limiter

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
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
app.include_router(health_router)


@app.get(
    "/",
    tags=["General"],
    summary="Home Endpoint",
    description="Returns a welcome message."
)
def home():
    return {
        "message": "Hello, Roshan! My first FastAPI app is running."
    }