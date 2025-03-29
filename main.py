from fastapi.responses import JSONResponse
import uvicorn

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import config
from app.routes import auth, categories, healthchecker, products
from app.schemas.response import ResponseSchema

app = FastAPI()


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

@app.exception_handler(HTTPException)
async def exception_handler(req: Request, ex: HTTPException):
    content = ResponseSchema(message=ex.detail, data={
            "method": req.method,
            "path": req.url.path,
        }).model_dump()

    return JSONResponse(
        status_code=ex.status_code,
        content=content
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=config.PORT,
        host=config.HOST,
        reload=config.RELOAD,
        log_level="info",
    )
