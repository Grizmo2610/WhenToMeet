from flask import Flask
from config import Config
from .routes import user_bp, meeting_bp
from flask import session, redirect, url_for
from functools import wraps

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return view(*args, **kwargs)
    return wrapped_view

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(user_bp)
    app.register_blueprint(meeting_bp)

    return app