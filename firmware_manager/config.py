import os

app_environment = os.environ.get("FLASK_ENV")
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URI", "postgresql://firmware:firmware@localhost:5432/firmware"
)

DEBUG = os.environ.get("DEBUG")
