from fastapi import APIRouter, Depends, status

from app.schemas.user import TokenSchema, UserDetail, UserLogin, UserSchema
from app.services.auth import AuthService
from app.services.dependencies import get_user_service


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/signup", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, auth_service=Depends(get_user_service)):
    return await auth_service.signup(body)


@router.post("/login", response_model=TokenSchema)
async def login(
    body: UserLogin,
    auth_service=Depends(get_user_service),
):
    return await auth_service.login(body)


@router.get("/me", response_model=UserDetail)
async def user_me(current_user: UserDetail = Depends(AuthService.get_current_user)):
    return current_user
