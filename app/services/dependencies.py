from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.repository.user import UserRepository
from app.services.auth import AuthService


async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return AuthService(db, user_repository)
