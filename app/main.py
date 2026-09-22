from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

import logging
import time
import uuid

from app.api.v1.health import router as health_router
from app.api.v1.summary import router as summary_router
from app.core.exception_handlers import app_exception_handler
from app.core.exceptions import AppException
from app.core.limiter import limiter
from app.core.logging_config import setup_logging
from app.exceptions.handlers import generic_exception_handler
from app.models.schemas import HomeResponse
from app.config.settings import settings

# configure logging
setup_logging()

logger = logging.getLogger(__name__)

# create FastAPI app
app = FastAPI(
    title="AI Text Summarizer API",
    description="""
    ## AI Text Summarizer API

    An AI-powered REST API for generating concise summaries from long-form text.

    ### Features

    - Multiple summary styles: short, bullet, and detailed
    - Google Gemini-powered summarization
    - Input validation and sanitization
    - Response caching
    - Rate limiting
    - Health monitoring
    - Structured error handling
    - Request tracing and processing-time tracking

    ### API Version

    Current API version: **v1**
    """,
    version="1.0.0",
    contact={
        "name": "Roshan Kumar",
        "url": "https://github.com/Roshan-08",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_origin,
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "detail": str(exc)
        }
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
    rate_limit_handler
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
    response_model=HomeResponse,
    tags=["General"],
    summary="API Welcome",
    description="""
Returns a welcome message confirming that the AI Text Summarizer API is running.

Use this endpoint as a basic connectivity check for the API.
""",
    response_description="API welcome message."
)
def home():
    return {
        "message": "Hello, Roshan! My first FastAPI app is running."
    }