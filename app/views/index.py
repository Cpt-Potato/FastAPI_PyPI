from fastapi import APIRouter, Depends

from ..core.config import templates
from ..core.security import is_logged_in_from_cookie
from ..db.models import Project, Release, User

router = APIRouter()


@router.get("/")
async def index(context: dict = Depends(is_logged_in_from_cookie)):
    projects = await Project.objects.limit(5).all()
    project_count = f"{await Project.objects.count():,}"
    release_count = f"{await Release.objects.count():,}"
    user_count = f"{await User.objects.count():,}"
    context.update(
        {
            "project_count": project_count,
            "release_count": release_count,
            "user_count": user_count,
            "projects": projects,
        }
    )
    return templates.TemplateResponse("index/index.html", context)
