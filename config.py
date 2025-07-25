# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv
import tempfile

load_dotenv()

class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "default-key")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_PATH", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    UPLOAD_FOLDER: str = tempfile.gettempdir() 