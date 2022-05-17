from fastapi import APIRouter, Depends

from ..core.config import templates
from ..core.security import is_logged_in_from_cookie
from ..db.models import Project

router = APIRouter()


@router.get("/{project_name}")
async def get_projects(
    project_name: str,
    context: dict = Depends(is_logged_in_from_cookie)
):
    project = await Project.objects.get_or_none(pk=project_name)
    latest_release = await project.project_releases.order_by("-version").first()
    context.update(
        {
            "project": project,
            "latest_release": latest_release,
            "is_latest": True
        }
    )
    return templates.TemplateResponse("/project/details.html", context)
