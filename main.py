import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import config
from app.routes import auth, healthchecker

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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=config.PORT,
        host=config.HOST,
        reload=config.RELOAD,
        log_level="info",
    )
