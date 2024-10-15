from fastapi import APIRouter
from app.core.config import settings


router = APIRouter()



@router.get("/health-check/")
async def health_check() -> bool:
    print("----------------------------")
    print(settings.all_cors_origins)
    print("----------------------------")

    return True
