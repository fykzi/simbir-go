import os

from dotenv import load_dotenv

load_dotenv()


ALLOW_ORIGINS = ["*"]
ALLOW_CREDENTIALS = True
ALLOW_METHODS = ["*"]
ALLOW_HEADERS = ["*"]


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", default="")


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
