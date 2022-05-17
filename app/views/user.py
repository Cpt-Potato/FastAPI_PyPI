from fastapi import APIRouter, Depends, Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from ..core.config import templates
from ..core.security import (authenticate_user, get_password_hash,
                             is_logged_in_from_cookie,
                             set_cookie_and_redirect_to_account)
from ..db.models import User

router = APIRouter()


@router.get("/account")
async def account(context: dict = Depends(is_logged_in_from_cookie)):
    if not context.get("is_logged_in"):
        return RedirectResponse(url="/user/login")
    return templates.TemplateResponse("user/account.html", context)


# ------ LOGIN ------

@router.get("/login")
async def login_get(
    request: Request, context: dict = Depends(is_logged_in_from_cookie)
):
    context["request"] = request
    return templates.TemplateResponse("user/login.html", context)


@router.post("/login")
async def login_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    context = {"request": request, "email": email}
    if not await authenticate_user(email, password):
        context["error"] = "The user does not exist or the password is wrong."
        return templates.TemplateResponse("user/login.html", context)
    return await set_cookie_and_redirect_to_account(email)


# ------ REGISTER ------

@router.get("/register")
async def register_get(
    request: Request, context: dict = Depends(is_logged_in_from_cookie)
):
    context["request"] = request
    return templates.TemplateResponse("user/register.html", context)


@router.post("/register")
async def register_post(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    is_in_db = await User.objects.get_or_none(email=email)
    if is_in_db:
        context = {
            "request": request,
            "email": email,
            "password": password,
            "error": "Email is already in use."
        }
        return templates.TemplateResponse("user/register.html", context)
    await User(
        email=email, hashed_password=get_password_hash(password)
    ).save()
    return await set_cookie_and_redirect_to_account(email)


# ------ LOGOUT ------

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="email")
    return response
