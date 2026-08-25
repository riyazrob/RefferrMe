from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import init_db
from app.routers import auth, endorsements, referrals, requests, users, waitlist

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Security: prevent accidental production start with default secret
    if not settings.debug and settings.secret_key == "change-me-in-production":
        raise RuntimeError(
            "Refusing to start: SECRET_KEY is default and DEBUG is False. Set a secure SECRET_KEY before deploying."
        )
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(users.router)
app.include_router(users.notifications_router)
app.include_router(auth.router)
app.include_router(auth.profile_router)
app.include_router(endorsements.router)
app.include_router(referrals.router)
app.include_router(requests.router)
app.include_router(waitlist.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"title": "Reffery"})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"title": "Dashboard"})


@app.get("/docs-ui", response_class=HTMLResponse)
def docs_ui(request: Request):
    return RedirectResponse(url="/docs")
