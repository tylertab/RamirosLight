from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.routes import (
    accounts,
    athletes,
    events,
    federations,
    health,
    news,
    rosters,
    search,
    subscriptions,
)
from app.core.config import SettingsSingleton
from app.core.database import init_models


def create_app() -> FastAPI:
    settings = SettingsSingleton().instance
    application = FastAPI(title=settings.project_name, version="1.0.0")

    base_dir = Path(__file__).resolve().parent
    template_dir = base_dir / "app" / "web" / "templates"
    templates = None
    index_markup = ""
    try:
        templates = Jinja2Templates(directory=str(template_dir))
    except AssertionError:
        templates = None
    if not templates and template_dir.exists():
        index_path = template_dir / "index.html"
        if index_path.exists():
            index_markup = index_path.read_text(encoding="utf-8")
    if not index_markup:
        index_markup = "<h1>Trackeo</h1>"
    static_dir = base_dir / "app" / "web" / "static"
    if static_dir.exists():
        application.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @application.get("/", response_class=HTMLResponse)
    async def render_index(request: Request) -> HTMLResponse:
        if templates is not None:
            return templates.TemplateResponse("index.html", {"request": request})
        return HTMLResponse(content=index_markup)

    application.include_router(health.router, prefix=settings.api_v1_prefix)
    application.include_router(accounts.router, prefix=settings.api_v1_prefix)
    application.include_router(subscriptions.router, prefix=settings.api_v1_prefix)
    application.include_router(athletes.router, prefix=settings.api_v1_prefix)
    application.include_router(events.router, prefix=settings.api_v1_prefix)
    application.include_router(rosters.router, prefix=settings.api_v1_prefix)
    application.include_router(news.router, prefix=settings.api_v1_prefix)
    application.include_router(search.router, prefix=settings.api_v1_prefix)
    application.include_router(federations.router, prefix=settings.api_v1_prefix)

    @application.on_event("startup")
    async def _create_tables() -> None:
        await init_models()

    return application


app = create_app()
