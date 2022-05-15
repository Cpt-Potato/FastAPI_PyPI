import base64

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from ..core.config import templates
from ..core.security import (authenticate_user, get_password_hash,
                             get_user_email_from_cookie)
from ..db.models import User

router = APIRouter()


@router.get("/account")
async def account(request: Request):
    email = await get_user_email_from_cookie(request)
    if not email:
        return RedirectResponse(url="/user/login", status_code=301)
    context = {"request": request, "email": email, "is_logged_in": True}
    return templates.TemplateResponse("user/account.html", context)


# ------ LOGIN ------

@router.get("/login")
async def login_get(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("user/login.html", context)


@router.post("/login")
async def login_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    context = {"request": request, "email": email}
    if not await authenticate_user(email, password):
        context["error"] = "The user does not exist or the password is wrong."
        return templates.TemplateResponse("user/login.html", context)
    response = RedirectResponse("/user/account", status_code=301)
    response.set_cookie(
        key="email",
        value=base64.b64encode(email.encode()).decode(),
        max_age=3600
    )
    return response


# ------ REGISTER ------

@router.get("/register")
async def register_get(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("user/register.html", context)


@router.post("/register")
async def register_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    is_in_db = await User.objects.get_or_none(email=email)
    if not is_in_db:
        # create a new user
        await User(
            email=email, hashed_password=get_password_hash(password)
        ).save()
        context = {"request": request, "email": email}
        return templates.TemplateResponse("user/account.html", context)

    context = {
        "request": request,
        "email": email,
        "error": "Email is already in use."
    }
    return templates.TemplateResponse("user/register.html", context)


# ------ LOGOUT ------

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="email")
    return response
