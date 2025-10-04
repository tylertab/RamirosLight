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

    def _template_response(
        request: Request,
        template_name: str,
        *,
        page_id: str,
        fallback_markup: str,
        context: dict[str, object] | None = None,
    ) -> HTMLResponse:
        if templates is not None:
            template_context: dict[str, object] = {"request": request, "page_id": page_id}
            if context:
                template_context.update(context)
            return templates.TemplateResponse(template_name, template_context)
        return HTMLResponse(content=fallback_markup)

    @application.get("/", response_class=HTMLResponse)
    async def render_index(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "index.html",
            page_id="home",
            fallback_markup=index_markup,
        )

    @application.get("/profiles", response_class=HTMLResponse)
    async def render_profiles(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "profiles.html",
            page_id="profiles",
            fallback_markup="<h1>Profiles</h1>",
        )

    @application.get("/athletes/{athlete_id}", response_class=HTMLResponse)
    async def render_athlete_detail(request: Request, athlete_id: int) -> HTMLResponse:
        return _template_response(
            request,
            "athlete_detail.html",
            page_id="athlete-detail",
            fallback_markup=f"<h1>Athlete #{athlete_id}</h1>",
            context={"athlete_id": athlete_id},
        )

    @application.get("/events", response_class=HTMLResponse)
    async def render_events_page(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "events.html",
            page_id="events",
            fallback_markup="<h1>Events</h1>",
        )

    @application.get("/rosters", response_class=HTMLResponse)
    async def render_rosters_page(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "rosters.html",
            page_id="rosters",
            fallback_markup="<h1>Rosters</h1>",
        )

    @application.get("/rosters/{roster_id}", response_class=HTMLResponse)
    async def render_roster_detail(request: Request, roster_id: int) -> HTMLResponse:
        return _template_response(
            request,
            "roster_detail.html",
            page_id="roster-detail",
            fallback_markup=f"<h1>Roster #{roster_id}</h1>",
            context={"roster_id": roster_id},
        )

    @application.get("/login", response_class=HTMLResponse)
    async def render_login(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "login.html",
            page_id="login",
            fallback_markup="<h1>Login</h1>",
        )

    @application.get("/signup", response_class=HTMLResponse)
    async def render_signup(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "signup.html",
            page_id="signup",
            fallback_markup="<h1>Sign up</h1>",
        )

    @application.get("/federations/upload", response_class=HTMLResponse)
    async def render_federations_upload(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "federations_upload.html",
            page_id="federations-upload",
            fallback_markup="<h1>Federations upload</h1>",
        )

    @application.get("/about", response_class=HTMLResponse)
    async def render_about(request: Request) -> HTMLResponse:
        return _template_response(
            request,
            "about.html",
            page_id="about",
            fallback_markup="<h1>About Trackeo</h1>",
        )

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
