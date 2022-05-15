from fastapi import APIRouter
from fastapi.requests import Request

from ..core.config import templates
from ..core.security import get_user_email_from_cookie
from ..db.models import Project, Release, User

router = APIRouter()


@router.get("/")
async def index(request: Request):
    projects = await Project.objects.limit(5).all()
    project_count = f"{await Project.objects.count():,}"
    release_count = f"{await Release.objects.count():,}"
    user_count = f"{await User.objects.count():,}"
    context = {
        "request": request,
        "is_logged_in": False,
        "project_count": project_count,
        "release_count": release_count,
        "user_count": user_count,
        "projects": projects
    }

    email = await get_user_email_from_cookie(request)
    if email:
        context["is_logged_in"] = True

    return templates.TemplateResponse("index/index.html", context)
