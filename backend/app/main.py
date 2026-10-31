from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.api import auth, curriculum, labs, progress, cheatsheets, assessments

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(curriculum.router, prefix="/api/v1")
app.include_router(labs.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")
app.include_router(cheatsheets.router, prefix="/api/v1")
app.include_router(assessments.router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
