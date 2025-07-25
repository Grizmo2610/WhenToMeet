from flask import Flask
from config import Config
from .routes import user_bp, meeting_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(user_bp)
    app.register_blueprint(meeting_bp)

    return app