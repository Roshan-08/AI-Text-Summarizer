# AI Text Summarizer

An AI-powered REST API that generates concise summaries from long-form text using **Google Gemini** and **FastAPI**.

This project demonstrates how to build a production-oriented GenAI backend with input validation, text sanitization, response caching, rate limiting, structured error handling, logging, API documentation, automated testing, security controls, and Docker support.

## Overview

The AI Text Summarizer accepts text through a REST API and generates summaries in different formats based on the requested style.

### Supported Summary Styles

* **Short** — Concise summary
* **Bullet** — Key points in bullet format
* **Detailed** — More comprehensive summary

The application follows a layered architecture that separates API routes, business logic, validation, configuration, services, and utilities.

## Features

* **AI-powered summarization** — Generates summaries using Google Gemini.
* **Multiple summary styles** — Supports short, bullet-point, and detailed summaries.
* **Input validation** — Validates request structure, text length, and summary style.
* **Text sanitization** — Removes HTML content and normalizes user input before processing.
* **Response caching** — Uses TTL-based in-memory caching to reduce repeated AI requests.
* **Cache protection** — Uses SHA-256 cache keys and configurable cache size limits.
* **Rate limiting** — Limits summarization requests to help prevent excessive API usage.
* **Structured API responses** — Uses consistent response models across endpoints.
* **Structured error handling** — Returns controlled responses for application errors and unexpected failures.
* **Security-focused error handling** — Prevents internal exception details and sensitive information from being exposed.
* **Request tracing** — Generates a unique request ID for every request.
* **Performance tracking** — Records request processing time through response headers.
* **Secure logging** — Avoids logging complete user-provided text.
* **Configurable CORS** — Frontend origin is controlled through environment configuration.
* **Environment-based configuration** — API credentials and application settings are loaded from environment variables.
* **API versioning** — Uses `/v1` to support future API evolution.
* **OpenAPI documentation** — Provides interactive Swagger UI documentation through FastAPI.
* **Automated testing** — Includes endpoint, validation, caching, configuration, error-handling, security, and OpenAPI tests.
* **100% code coverage** — Current test suite contains **49 passing tests** with **100% code coverage**.
* **Docker support** — Application can be built and run as a Docker container.

## Tech Stack

### Backend

* **Python 3.14** — Core programming language
* **FastAPI** — REST API framework
* **Pydantic** — Request and response validation
* **Pydantic Settings** — Environment-based configuration
* **Google Gemini** — Large language model for summarization
* **SlowAPI** — API rate limiting
* **Uvicorn** — ASGI server

### Testing

* **Pytest** — Automated testing framework
* **Pytest-Cov** — Code coverage reporting

### Development & Infrastructure

* **Git & GitHub** — Version control and source management
* **Docker** — Containerization
* **VS Code** — Development environment
* **OpenAPI / Swagger UI** — Interactive API documentation

## Architecture

The application follows a layered backend architecture where each component has a specific responsibility.

```text
                         Client
                           │
                           ▼
                  FastAPI Application
                           │
                           ▼
                    API Router (/v1)
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Validation   Rate Limiting   Sanitization
              │
              ▼
         Summary Service
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
      Cache     Gemini API
        │           │
        └─────┬─────┘
              ▼
       Structured Response
              │
              ▼
            Client
```

## Project Structure

```text
AI-Text-Summarizer/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       └── summary.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── core/
│   │   ├── exception_handlers.py
│   │   ├── exceptions.py
│   │   ├── limiter.py
│   │   └── logging_config.py
│   │
│   ├── exceptions/
│   │   └── handlers.py
│   │
│   ├── models/
│   │   ├── api_response.py
│   │   └── schemas.py
│   │
│   ├── prompts/
│   │   └── summary_prompt.py
│   │
│   ├── services/
│   │   └── summarizer.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── text.py
│   │
│   ├── validation/
│   │   └── text_validator.py
│   │
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_openapi.py
│   ├── test_settings.py
│   ├── test_summarizer.py
│   └── test_summary.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── pytest.ini
└── requirements.txt
```

## How It Works

The summarization request passes through several layers before reaching the AI model.

1. **Client sends a request**

   * The client sends text and a summary style to `POST /v1/summarize`.

2. **Request validation**

   * Pydantic validates the request structure.
   * Supported summary styles are validated.
   * Input length limits are enforced.

3. **Input sanitization**

   * HTML content is removed.
   * Extra whitespace and unnecessary formatting are normalized.

4. **Rate limiting**

   * Requests are limited to help protect the API from excessive usage.

5. **Cache lookup**

   * The service checks whether a valid cached summary exists for the same text and style.
   * SHA-256 is used to generate the cache key.
   * Expired entries are removed.
   * Cache size is limited to prevent unbounded memory growth.

6. **AI summarization**

   * If no valid cached result exists, the request is passed to the summarization service.
   * The service sends the prepared prompt to Google Gemini.

7. **Response generation**

   * The generated summary is returned through a structured API response.
   * Response metadata includes word count, model name, and processing time.

8. **Observability**

   * Each request receives a unique request ID.
   * Processing time and important application events are logged.
   * User-provided text is not written to application logs.

## API Endpoints

| Method | Endpoint        | Description                     |
| ------ | --------------- | ------------------------------- |
| `GET`  | `/`             | Returns basic API information   |
| `GET`  | `/v1/health`    | Checks application health       |
| `POST` | `/v1/summarize` | Generates an AI-powered summary |

### Interactive API Documentation

After starting the application, open:

```text
http://localhost:8000/docs
```

FastAPI also provides the raw OpenAPI specification at:

```text
http://localhost:8000/openapi.json
```

## API Example

### Request

`POST /v1/summarize`

```json
{
  "text": "Artificial Intelligence is transforming healthcare by improving disease diagnosis, supporting medical professionals, and enabling more efficient analysis of large amounts of medical data.",
  "style": "short"
}
```

### Response

```json
{
  "success": true,
  "message": "Summary generated successfully.",
  "data": {
    "summary": "Artificial Intelligence is transforming healthcare by improving disease diagnosis.",
    "word_count": 9,
    "model_used": "gemini-3.6-flash",
    "processing_time_ms": 1250.42
  }
}
```

## Local Development

### Prerequisites

Make sure the following are installed:

* Python 3.14+
* Git
* A Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/Roshan-08/AI-Text-Summarizer.git
cd AI-Text-Summarizer
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as the template:

```text
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-3.6-flash
API_VERSION=v1
CACHE_TTL=300
CACHE_MAX_SIZE=100
MAX_INPUT_LENGTH=5000
```

Do not commit the real `.env` file to Git.

### 5. Start the Application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Docker

The application includes a Dockerfile for containerized execution.

### Build the Image

```powershell
docker build -t ai-text-summarizer .
```

### Run the Container

Pass environment variables from the local `.env` file:

```powershell
docker run --name ai-text-summarizer-container --env-file .env -p 8000:8000 ai-text-summarizer
```

The API will then be available at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/v1/health
```

Swagger UI:

```text
http://localhost:8000/docs
```

The API key is provided to the container at runtime and is not baked into the Docker image.

## Testing & Quality

The project includes automated tests covering:

* Health endpoints
* API responses
* Request validation
* Input sanitization
* Summary generation
* Summary service failures
* Rate limiting
* Cache behavior
* Cache expiration
* Cache size protection
* Cache key hashing
* Configuration validation
* CORS behavior
* Error handling
* Internal error protection
* Logging security
* OpenAPI documentation

### Run Tests

```powershell
python -m pytest -v
```

Current result:

```text
49 passed
```

### Run Tests with Coverage

```powershell
python -m pytest --cov --cov-report=term-missing
```

Current coverage:

```text
TOTAL    610 statements    0 missed    100%
```

## Security

The project includes several security-focused controls:

* API credentials are loaded through environment variables.
* `.env` is excluded from Git.
* User-provided text is not written to application logs.
* Cache keys use SHA-256 rather than storing raw input text.
* In-memory cache size is bounded.
* Cache entries expire using TTL.
* API requests are rate limited.
* CORS allows only the configured frontend origin.
* Internal exception details are hidden from API responses.
* Input length is bounded to prevent excessively large requests.
* Supported summary styles are restricted through validation.

These controls provide a security-conscious foundation for further production hardening.

## Future Improvements

Planned improvements include:

* Add GitHub Actions for continuous integration.
* Build a production-ready frontend interface.
* Deploy the API to a cloud platform.
* Add persistent usage analytics.
* Replace the in-memory cache with Redis for distributed deployments.
* Add authentication and authorization for protected API usage.
* Improve production monitoring and observability.
* Expand integration and edge-case testing.
* Perform a final production deployment and security review.

## Author

**Roshan Kumar**

GitHub: `https://github.com/Roshan-08`
