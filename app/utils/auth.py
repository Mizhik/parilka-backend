from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, ExpiredSignatureError
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.core.settings import config

security = HTTPBearer()


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    @staticmethod
    async def create_access_token(data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, config.AUTH_SECRET_KEY, algorithm=config.AUTH_ALGORITHM
        )
        return encoded_access_token

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
            email = payload.get("sub")
            if email is None:
                raise credentials_exception
            return email

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
