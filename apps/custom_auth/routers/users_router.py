from typing import Annotated, Optional
from datetime import datetime, timedelta

from bcrypt import checkpw
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm
)
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse
from fastapi import Form

from core.db import get_session
from apps.custom_auth.schemas.users_schemas import Token, TokenData, UserCreate, UserModel
from apps.custom_auth.queries.user_queries import create_user, get_users, get_user
from core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="apps/custom_auth/templates")


async def create_access_token(
    data: dict, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise exception
        token_data = TokenData(username=username)
    except JWTError:
        raise exception
    user = get_user(session=session, username=token_data.username)
    if not user:
        raise exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/", response_class=HTMLResponse)
async def get_user_list(
    request: Request,
    user: Annotated[Optional[UserModel], Depends()], 
    session: AsyncSession = Depends(get_session)
):
    users = await get_users(
        session=session, 
        user_id=user.user_id, 
        username=user.username, 
        email=user.email,
    )
    return templates.TemplateResponse(
        request, "index.html", {"users": users}
    )

@router.post("/sign-up", response_class=JSONResponse)
async def sign_up(
    request: Request,
    username: str = Form(...), 
    email: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    if password1 != password2:
        raise HTTPException(status_code=400, detail="Passwords are not the same")
    user_create = UserCreate(username=username, email=email, password1=password1, password2=password2)
    try:
        await create_user(user=user_create, session=session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(content={"message": "User created successfully", "username": username, "email": email})


@router.post("/sign-in")
async def sign_in(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session)
) -> Token:  
    user = await get_user(session=session, username=form.username)
    if not user:
        raise HTTPException(400, "Incorrect usernmame or password")
    if not checkpw(form.password.encode(), user.password.encode()):
        raise HTTPException(400, "Incorrect usernmame or password")
    access_token_expires = settings.ACCESS_TOKEN_EXPIRATION
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
