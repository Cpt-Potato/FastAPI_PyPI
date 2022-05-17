from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api import project_api, release_api, user_api
from .db.base import database
from .views import index, project, user

app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

# ------ API ------
app.include_router(user_api.router, prefix="/api", tags=["user"])
app.include_router(project_api.router, prefix="/api", tags=["project"])
app.include_router(release_api.router, prefix="/api", tags=["release"])

# ------ INDEX ------
app.include_router(index.router, tags=["index"], include_in_schema=False)

# ------ PROJECTS ------
app.include_router(project.router, prefix="/project", include_in_schema=False)

# ------ ACCOUNT ------
app.include_router(
    user.router, prefix="/user", tags=["account"], include_in_schema=False
)


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()
