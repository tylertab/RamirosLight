from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.routes import accounts, health, events, federations
from app.core.config import SettingsSingleton


def create_app() -> FastAPI:
    settings = SettingsSingleton().instance
    application = FastAPI(title=settings.project_name, version="1.0.0")

    base_dir = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(base_dir / "app" / "web" / "templates"))
    static_dir = base_dir / "app" / "web" / "static"
    if static_dir.exists():
        application.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @application.get("/", response_class=HTMLResponse)
    async def render_index(request: Request) -> HTMLResponse:
        return templates.TemplateResponse("index.html", {"request": request})

    application.include_router(health.router, prefix=settings.api_v1_prefix)
    application.include_router(accounts.router, prefix=settings.api_v1_prefix)
    application.include_router(events.router, prefix=settings.api_v1_prefix)
    application.include_router(federations.router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
