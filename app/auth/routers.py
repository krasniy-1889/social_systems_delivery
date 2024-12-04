from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from app.auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.auth.exceptions import UserAlreadyExists
from app.auth.schemas import Token, UserAddDTO, UserDTO
from app.auth.service import AuthService
from app.loggers import set_logger
from app.utils.dependencies import UOWDep

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

set_logger(__name__)


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UOWDep,
) -> Token:
    user = await authenticate_user(uow, form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserDTO)
async def read_users_me(
    current_user: Annotated[UserDTO, Depends(get_current_user)],
):
    return current_user


@router.post(
    "/register",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user: UserAddDTO,
    uow: UOWDep,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    user_username = await auth_service.find_one(uow, username=user.username)
    logger.debug(user_username)
    if user_username:
        raise UserAlreadyExists

    user = await auth_service.add_user(uow, user)
    return user
