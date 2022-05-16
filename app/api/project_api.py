from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..db.models import Project
from ..schemas import (ProjectDelete, ProjectIn, ProjectOut,
                       ProjectOutNoDescription, ProjectUpdate)

router = APIRouter()


@router.get(
    "/projects",
    response_model=list[ProjectOutNoDescription],
    response_model_exclude={"description"},
    name="Show all projects and releases"
)
async def get_projects(page: int = 1):
    return await (
        Project.objects.select_all()
        .exclude_fields(["description"])
        .paginate(page=page, page_size=10)
        .all()
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
