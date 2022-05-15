import ormar

from .base import database, metadata


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(MainMeta):
        tablename = "users"

    id = ormar.Integer(primary_key=True)
    email = ormar.String(max_length=50, unique=True)
    hashed_password = ormar.String(max_length=100)


class Project(ormar.Model):
    class Meta(MainMeta):
        tablename = "projects"

    id = ormar.String(primary_key=True, unique=True, max_length=50)
    summary = ormar.Text(nullable=True)
    description = ormar.Text(nullable=True)
    homepage = ormar.String(max_length=50, nullable=True)
    license = ormar.String(max_length=50, nullable=True)
    author = ormar.String(max_length=50, nullable=True)

    user_id = ormar.ForeignKey(
        User, related_name="user_projects", nullable=True
    )


class Release(ormar.Model):
    class Meta(MainMeta):
        tablename = "releases"

    id = ormar.Integer(primary_key=True)
    version = ormar.String(max_length=20, default="0.0.1")
    created_date = ormar.DateTime()

    project_id = ormar.ForeignKey(
        Project, related_name="project_releases", nullable=False
    )
