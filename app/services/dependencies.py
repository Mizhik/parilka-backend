from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.repository.category import CategoryRepository
from app.repository.liquids import LiquidsRepository
from app.repository.product import ProductRepository
from app.repository.user import UserRepository
from app.services.auth import AuthService
from app.services.liquids import LiquidsService
from app.services.product import ProductService
from app.services.category import CategoryService


async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return AuthService(db, user_repository)


async def get_product_service(db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    return ProductService(db, product_repository)

async def get_category_service(db: AsyncSession = Depends(get_db)):
    category_repository = CategoryRepository(db)
    return CategoryService(db, category_repository)

async def get_liquids_service(db: AsyncSession = Depends(get_db)):
    liquids_service = LiquidsRepository(db)
    return LiquidsService(db, liquids_service)
