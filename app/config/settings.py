import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.6-flash"
)

CACHE_TTL = int(
    os.getenv(
        "CACHE_TTL",
        300
    )
)

API_VERSION = "v1"

MAX_INPUT_LENGTH = 5000