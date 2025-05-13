"""
ONLY FOR TEST PURPOSES

!! DO NOT USE IN PRODUCTION !!

"""

from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.core.settings import config
from app.routes import (
    auth,
    categories,
    countries,
    healthchecker,
    products,
    subcategories,
    manufacturers,
)
from app.schemas.response import ResponseSchema
from app.services.errors import BaseHTTPError


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield


app = FastAPI(
    docs_url=None,
    openapi_url=None,
    redoc_url=None,
    redirect_slashes=False,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthchecker.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(subcategories.router)
app.include_router(manufacturers.router)
app.include_router(countries.router)


@app.exception_handler(BaseHTTPError)
async def exception_handler(req: Request, ex: HTTPException):
    content = ResponseSchema(
        message=ex.detail,
        data={
            "method": req.method,
            "path": req.url.path,
        },
    ).model_dump()

    return JSONResponse(status_code=ex.status_code, content=content)
