from fastapi.responses import JSONResponse
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.core import settings
from app.core.settings import config
from app.routes import auth, categories, constructor, healthchecker, products
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
app.include_router(constructor.router)

@app.exception_handler(BaseError)
async def exception_handler(req: Request, ex: HTTPException):
    content = ResponseSchema(message=ex.detail, data={
            "method": req.method,
            "path": req.url.path,
        }).model_dump()

    return JSONResponse(
        status_code=ex.status_code,
        content=content
    )


security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = settings.config.DOCS_USER
    password = settings.config.DOCS_PASSWORD
    if not(credentials.username == username and credentials.password == password):
        raise LoginFailed()
    return credentials.username

@app.get("/docs", include_in_schema=False)
async def get_docs(_: str = Depends(get_current_user)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/openapi.json", include_in_schema=False)
async def get_oapi(_: str = Depends(get_current_user)):
    return get_openapi(title = "FastAPI", version="0.1.0", routes=app.routes)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=config.PORT,
        host=config.HOST,
        reload=config.RELOAD,
        log_level="info",
    )
