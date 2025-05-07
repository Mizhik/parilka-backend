from fastapi.responses import JSONResponse
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.core import settings
from app.core.settings import config
from app.routes import auth, categories, healthchecker, products, subcategories
from app.schemas.response import ResponseSchema
from app.services.errors import BaseError, LoginFailed

app = FastAPI(docs_url=None, openapi_url=None, redoc_url=None)


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
