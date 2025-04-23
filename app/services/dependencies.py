from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.repository.category import CategoryRepository
from app.repository.constructor import ConstructorRepository
from app.repository.devices import DevicesRepository
from app.repository.liquids import LiquidsRepository
from app.repository.product import ProductRepository
from app.repository.user import UserRepository
from app.services.auth import AuthService
from app.services.devices import DevicesService
from app.services.liquids import LiquidsService
from app.services.product import ProductService
from app.services.category import CategoryService
from app.services.constructor import ConstructorService


async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return AuthService(db, user_repository)


async def get_product_service(db: AsyncSession = Depends(get_db)):
    product_repository = ProductRepository(db)
    return ProductService(db, product_repository)


async def get_category_service(db: AsyncSession = Depends(get_db)):
    category_repository = CategoryRepository(db)
    return CategoryService(db, category_repository)


async def get_constructor_service(db: AsyncSession = Depends(get_db)):
    constructor_repository = ConstructorRepository(db)
    return ConstructorService(db, constructor_repository)


async def get_liquids_service(db: AsyncSession = Depends(get_db)):
    liquids_service = LiquidsRepository(db)
    return LiquidsService(db, liquids_service)


async def get_devices_service(db: AsyncSession = Depends(get_db)):
    devices_service = DevicesRepository(db)
    return DevicesService(db, devices_service)
