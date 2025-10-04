from fastapi import APIRouter

from app.core.config import SettingsSingleton

router = APIRouter(tags=["health"])


@router.get("/health", summary="Readiness probe")
async def health_check() -> dict[str, str]:
    settings = SettingsSingleton().instance
    return {
        "service": settings.project_name,
        "status": "ok",
        "environment": settings.environment,
    }
