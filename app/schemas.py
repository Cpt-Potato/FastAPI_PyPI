from datetime import datetime

from pydantic import BaseModel

# # ------ USER ------
#
# UserIn = User.get_pydantic(exclude={"user_projects"})
# UserOut_ProjectInfo = User.get_pydantic(exclude={"hashed_password"})
# UserUpdateOut = User.get_pydantic(exclude={"hashed_password", "user_projects"})
#
# # ------ PROJECT ------
#
# ProjectIn = Project.get_pydantic(
#     exclude={"project_releases", "user_id__email", "user_id__hashed_password"}
# )
# ProjectOut = Project.get_pydantic(exclude={"user_id__hashed_password"})
# UpdateProject = Project.get_pydantic(
#     exclude={"user_id__hashed_password", "project_releases"}
# )
# DeleteProject = Project.get_pydantic(
#     include={"id"}
# )
#
# ------ RELEASE ------
#
# ResponseReleaseIn = Release.get_pydantic(
#     include={"id", "name", "version", "created_date", "project_id__id"}
# )
# DeleteRelease = Release.get_pydantic(include={"id"})


class UserBase(BaseModel):
    id: int | None = None
    email: str | None = "user@example.com"


class UserUpdate(UserBase):
    password: str | None = "some_password"


class UserUpdateOut(UserBase):
    hashed_password: str


class UserIn(UserUpdate):
    pass


class UserOut(UserBase):
    pass


class UserCreateOut(UserUpdateOut):
    pass


class ReleaseBase(BaseModel):
    id: int
    name: str = "release"
    version: str = "0.0.1"
    created_date: datetime = datetime.utcnow()


class ReleaseIn(ReleaseBase):
    project_id: str = "project name"


class ProjectId(BaseModel):
    id: str = "project name"


class ReleaseOut(ReleaseBase):
    project_id: ProjectId


class ReleaseUpdate(ReleaseIn):
    pass


class ReleaseDelete(BaseModel):
    id: int


class ProjectBase(BaseModel):
    id: str = "project name"
    summary: str | None
    description: str | None
    homepage: str | None
    license: str | None
    author: str | None


class ProjectIn(ProjectBase):
    user_id: int


class ProjectAndReleases(ProjectBase):
    project_releases: list[ReleaseBase] | list = []


class ProjectOut(ProjectAndReleases):
    user_id: UserBase | None = None


class ProjectOutNoDescription(ProjectOut):
    description: str | None = "For description go to website"


class ProjectUpdate(ProjectBase):
    pass


class ProjectDelete(BaseModel):
    id: str = "project name"


class UserOutProjectInfo(UserBase):
    user_projects: list[ProjectAndReleases] | list = []
