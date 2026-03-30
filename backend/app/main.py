from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router
from app.api.routes.query import router as query_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name, version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "details": exc.details or None},
    )


app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(documents_router, prefix=settings.api_prefix)
app.include_router(query_router, prefix=settings.api_prefix)
