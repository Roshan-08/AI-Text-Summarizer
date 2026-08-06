from fastapi import APIRouter

router = APIRouter(
    prefix="/v1",
    tags=["Health"]
)

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }