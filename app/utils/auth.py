from datetime import datetime, timedelta
from typing import Literal, Optional
from fastapi import HTTPException, status
from jose import jwt, ExpiredSignatureError
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.core.settings import config

security = HTTPBearer()


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    @staticmethod
    async def create_token(
        data: dict,
        scope: Literal["access_token", "refresh_token"] = "access_token",
    ):
        to_encode = data.copy()
        if scope == "access_token":
            expire = datetime.now() + timedelta(
                minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        if scope == "refresh_token":
            expire = datetime.now() + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"iat": datetime.now(), "exp": expire, "scope": scope})
        encoded_token = jwt.encode(
            to_encode, config.AUTH_SECRET_KEY, algorithm=config.AUTH_ALGORITHM
        )
        return encoded_token

    @staticmethod
    async def create_access_token(data: dict):
        return await Auth.create_token(data, "access_token")

    @staticmethod
    async def create_refresh_token(data: dict):
        return await Auth.create_token(data, "refresh_token")

    @staticmethod
    async def get_current_user_with_token(token: str) -> Optional[tuple[str, str]]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                config.AUTH_SECRET_KEY,
                algorithms=[config.AUTH_ALGORITHM],
            )
            if payload.get("scope") != "access_token":
                raise credentials_exception
            email = payload.get("email")
            if email is None:
                raise credentials_exception
            return email

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def get_current_user_with_token_for_refresh(
        token: str,
    ) -> Optional[tuple[str, str]]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                config.AUTH_SECRET_KEY,
                algorithms=[config.AUTH_ALGORITHM],
            )
            if payload.get("scope") != "refresh_token":
                raise credentials_exception
            id = payload.get("sub")
            if id is None:
                raise credentials_exception
            return id

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
