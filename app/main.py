from dotenv import load_dotenv
load_dotenv()
import pathlib
import fastapi
import fastapi.staticfiles
import app.routes as routes


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"


PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


app = fastapi.FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator",
    version="1.0.0"
)


app.mount(
    "/static",
    fastapi.staticfiles.StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static"
)


app.include_router(
    routes.router
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "ComicCraft"
    }


@app.get("/api")
async def api_status():
    return {
        "status": "success",
        "message": "ComicCraft API is running"
    }