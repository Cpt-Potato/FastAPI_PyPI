import os

from dotenv import load_dotenv
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env.dev")
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DATABASE_URL")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("SECRET_KEY")
