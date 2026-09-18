# AI Text Summarizer

An AI-powered REST API that generates concise summaries from long-form text using Google Gemini and FastAPI.

The project demonstrates how to build a production-oriented GenAI backend with input validation, text sanitization, response caching, rate limiting, structured error handling, logging, API documentation, and automated testing.

## Overview

The AI Text Summarizer accepts text through a REST API and generates summaries in different formats based on the requested style.

Supported summary styles:

- Short
- Bullet
- Detailed

The application is built with a layered architecture to keep API routes, business logic, validation, configuration, and utilities separated and maintainable.

## Features

- **AI-powered summarization** — Generates summaries using Google Gemini.
- **Multiple summary styles** — Supports short, bullet-point, and detailed summaries.
- **Input validation** — Validates request data and enforces text length limits.
- **Text sanitization** — Removes HTML content and normalizes user input before AI processing.
- **Response caching** — Uses TTL-based in-memory caching to reduce unnecessary AI requests.
- **Rate limiting** — Limits summarization requests to protect the API from excessive usage.
- **Structured API responses** — Uses consistent response models across the API.
- **Error handling** — Provides structured responses for validation, rate-limit, and server errors.
- **Request tracing** — Generates request IDs to help trace individual API requests.
- **Performance tracking** — Records API processing time for each request.
- **Application logging** — Logs important application and request events for observability.
- **API versioning** — Uses `/v1` to support future API evolution.
- **OpenAPI documentation** — Automatically generates interactive API documentation with FastAPI.
- **Automated testing** — Includes API, validation, error-handling, caching, and OpenAPI tests.
- **100% test coverage** — Current test suite contains **36 passing tests** with **100% code coverage**.

## Tech Stack

### Backend

- **Python 3.14** - Core programming language
- **FastAPI** - REST API framework
- **Pydantic** - Request and response validation
- **Google Gemini** - Large language model for text summarization
- **SlowAPI** - API rate limiting

### Testing

- **Pytest** - Automated testing framework
- **Pytest-Cov** - Test coverage reporting

### Development & Tools

- **Git & GitHub** - Version control and source code management
- **VS Code** - Development environment
- **Uvicorn** - ASGI server
- **OpenAPI / Swagger UI** - Interactive API documentation

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
  ├── Request Validation
  │
  ├── Rate Limiting
  │
  └── Input Sanitization
          │
          ▼
     Summary Service
          │
     ┌────┴─────┐
     │          │
     ▼          ▼
   Cache    Gemini API
     │          │
     └────┬─────┘
          ▼
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
  ├── Request Validation
  │
  ├── Rate Limiting
  │
  └── Input Sanitization
          │
          ▼
     Summary Service
          │
     ┌────┴─────┐
     │          │
     ▼          ▼
   Cache    Gemini API
     │          │
     └────┬─────┘
          ▼
```markdown
   Summary Response
          │
          ▼
        Client

## How It Works

The summarization request flows through several layers before reaching the AI model.

1. **Client sends a request**
   - The client sends text and a summary style to `POST /v1/summarize`.

2. **Request validation**
   - Pydantic validates the request structure.
   - Text length and supported summary styles are checked.

3. **Input sanitization**
   - HTML content is removed.
   - Extra whitespace and unnecessary formatting are normalized.

4. **Rate limiting**
   - Requests are limited to protect the API from excessive usage.

5. **Cache lookup**
   - The application checks whether a recent summary already exists for the same input.
   - Cached results can avoid unnecessary AI API calls.

6. **AI summarization**
   - If no valid cached result exists, the request is passed to the summarization service.
   - The service sends the prepared prompt to Google Gemini.

7. **Response generation**
   - The generated summary is returned through a structured API response.
   - Response metadata includes word count, model used, and processing time.

8. **Observability**
   - Each request receives a request ID.
   - Processing time and important application events are logged.

## API Usage

### Start the Application

Activate the virtual environment and start the FastAPI server:

```bash
uvicorn app.main:app --reload

## Testing & Quality

The project includes an automated test suite covering API endpoints, validation, error handling, caching behavior, and OpenAPI documentation.

### Run Tests

```bash
pytest -v

## Environment Setup

The application uses environment variables for configuration and API credentials.

### 1. Clone the Repository

```bash
git clone https://github.com/Roshan-08/AI-Text-Summarizer.git
cd AI-Text-Summarizer

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns basic API information |
| `GET` | `/v1/health` | Checks application health |
| `POST` | `/v1/summarize` | Generates an AI-powered summary |

### Summarization Request

`POST /v1/summarize`

Request body:

```json
{
  "text": "Your text to summarize...",
  "style": "short"
}

## Future Improvements

Planned improvements for the project include:

- Add a production-ready frontend interface.
- Containerize the application using Docker.
- Add GitHub Actions for continuous integration and automated testing.
- Deploy the API to a cloud platform.
- Improve caching with a distributed cache such as Redis.
- Add persistent storage for usage analytics and application data.
- Improve monitoring and observability.
- Add authentication and authorization for protected API usage.
- Expand the test suite with additional edge cases and integration tests.
- Perform a production-focused security and configuration review.

## Author

**Roshan Kumar**