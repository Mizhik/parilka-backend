from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db

router = APIRouter(prefix="/healthchecker", tags=["healthchecker"])


@router.get("/")
async def root():
    return {"status_code": 200, "detail": "ok", "result": "working"}


@router.get("/db")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")