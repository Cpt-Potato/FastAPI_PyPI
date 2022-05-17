import base64
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from ..db.models import User
from ..schemas import UserIn, UserSecurityOut


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def set_cookie_and_redirect_to_account(email: str):
    response = RedirectResponse(
        "/user/account", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )
    response.set_cookie(
        key="email",
        value=base64.b64encode(email.encode()).decode(),
        max_age=3600
    )
    return response


async def get_user_email_from_cookie(request: Request) -> str | None:
    cookie_value = request.cookies.get("email")
    if not cookie_value:
        return None
    email = base64.b64decode(cookie_value.encode()).decode()
    return email


async def is_logged_in_from_cookie(request: Request) -> dict:
    has_cookie = await get_user_email_from_cookie(request)
    context = {"request": request, "email": has_cookie, "is_logged_in": True}
    if not has_cookie:
        context["is_logged_in"] = False
    return context


async def get_user_by_email(email: str) -> UserSecurityOut | None:
    return await User.objects.get_or_none(email=email)


async def authenticate_user(
    email: str, password: str
) -> UserSecurityOut | None:
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> UserSecurityOut | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
