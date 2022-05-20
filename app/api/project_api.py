from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ..core.security import get_current_user
from ..db.models import Project, User
from ..schemas import (ProjectDelete, ProjectIn, ProjectOut,
                       ProjectAndReleasesOutNoDescription, ProjectUpdate,
                       UserIn, UserOutProjectInfo)

router = APIRouter()


@router.get(
    "/projects",
    response_model=list[ProjectAndReleasesOutNoDescription],
    response_model_exclude={"description"},
    name="Show project and its releases"
)
async def get_project_and_releases(project_name: str):
    return await (
        Project.objects.select_all()
        .exclude_fields(["description"])
        .filter(pk=project_name)
        .all()
    )


@router.get("/project/me", response_model=UserOutProjectInfo)
async def get_own_projects(current_user: UserIn = Depends(get_current_user)):
    return await (
        User.objects
            .select_all(follow=True)
            .get_or_none(email=current_user.email)
    )


@router.post(
    "/project",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED
)
async def create_project(project: ProjectIn):
    return await Project(**project.dict()).save()


@router.put("/project", response_model=ProjectOut)
async def update_project(project: ProjectUpdate):
    project = project.dict(exclude_unset=True, exclude_defaults=True)
    is_in_db = await (
        Project.objects.select_all().get_or_none(pk=project.get("id")))
    if not is_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await is_in_db.update(**project)


@router.delete("/project")
async def delete_project(project: ProjectDelete):
    is_in_db = await Project.objects.get_or_none(pk=project.dict().get("id"))
    if not is_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await is_in_db.delete()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="OK")
