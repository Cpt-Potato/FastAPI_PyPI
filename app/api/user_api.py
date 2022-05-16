from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..core.security import (Token, authenticate_user, create_access_token,
                             get_current_user, get_password_hash)
from ..db.models import User
from ..schemas import (UserCreateOut, UserIn, UserOut, UserOutProjectInfo,
                       UserUpdate, UserUpdateOut)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/users", response_model=list[UserOut], name="Show all users"
)
async def get_users():
    return await User.objects.all()


@router.get(
    "/user/{user_id}",
    response_model=UserOutProjectInfo,
    name="Get info by user id"
)
async def get_user_by_id(user_id: int):
    """ Get full info by user id (including projects and releases) """
    user = await User.objects.select_all(follow=True).get_or_none(pk=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.get("/user/me/projects", response_model=UserOutProjectInfo)
async def get_own_projects(current_user: UserIn = Depends(get_current_user)):
    return await (
        User.objects
            .select_all(follow=True)
            .get_or_none(email=current_user.email)
    )


@router.post(
    "/user",
    response_model=UserCreateOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserIn):
    new_user = User(**user.dict())
    is_in_db = await User.objects.get_or_none(email=new_user.email)
    if is_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use"
        )
    new_user.hashed_password = get_password_hash(new_user.hashed_password)
    return await new_user.save()


@router.put("/user", response_model=UserUpdateOut)
async def update_user(
    user: UserUpdate, current_user=Depends(get_current_user)
):
    new_data = user.dict(exclude_unset=True, exclude_defaults=True)
    if new_data.get("id") != current_user.id:
        raise HTTPException(
            status_code=401, detail="You can only update your information"
        )
    new_data_password = new_data.get("password")
    if new_data_password:
        new_password = get_password_hash(new_data_password)
        new_data["hashed_password"] = new_password
        new_data.pop("password")
    return await current_user.update(**new_data)


@router.delete("/user", name="Delete your account")
async def delete_user(current_user=Depends(get_current_user)):
    """ User can be deleted only if he has no projects """
    await current_user.delete()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="OK")
