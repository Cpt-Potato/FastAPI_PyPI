from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..db.models import Release
from ..schemas import ReleaseDelete, ReleaseIn, ReleaseOut, ReleaseUpdate

router = APIRouter()


@router.get("/releases", response_model=list[ReleaseOut])
async def get_releases():
    return await Release.objects.all()


@router.post(
    "/release",
    response_model=ReleaseOut,
    status_code=status.HTTP_201_CREATED
)
async def create_release(release: ReleaseIn):
    release = Release(**release.dict())
    return await release.save()


@router.put("/release", response_model=ReleaseOut)
async def update_release(release: ReleaseUpdate):
    release = release.dict(exclude_unset=True, exclude_defaults=True)
    is_in_db = await Release.objects.get_or_none(name=release.get("name"))
    if not is_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await is_in_db.update(**release)


@router.delete("/release")
async def delete_release(release: ReleaseDelete):
    is_in_db = await Release.objects.get_or_none(pk=release.dict().get("id"))
    if not is_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await is_in_db.delete()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="OK")
