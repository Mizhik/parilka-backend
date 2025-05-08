from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import config
from app.routes import auth, categories, countries, healthchecker, products, subcategories, manufacturers

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
app.include_router(manufacturers.router)
app.include_router(countries.router)
