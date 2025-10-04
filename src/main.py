from fastapi import FastAPI

from app.api.v1.routes import accounts, health, events, federations
from app.core.config import SettingsSingleton


def create_app() -> FastAPI:
    settings = SettingsSingleton().instance
    application = FastAPI(title=settings.project_name, version="1.0.0")

    application.include_router(health.router, prefix=settings.api_v1_prefix)
    application.include_router(accounts.router, prefix=settings.api_v1_prefix)
    application.include_router(events.router, prefix=settings.api_v1_prefix)
    application.include_router(federations.router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
