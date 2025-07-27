from flask import Blueprint, Response, redirect, url_for, request, session, jsonify
from app.models import User, Database
from app.ultils import *

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route('/api/login', methods=['POST'])
def login() -> Response:
    email: str | None = request.form.get('email', type=str)
    password: str | None = request.form.get('password')
    db = Database()
    user: User = User(db)
    user_data = user.login(email, password)
    if user_data['status'] == 200:
        session.permanent = True
        session['user_id'] = user_data['id']
        session['username'] = user_data['username']
    return jsonify(user_data)


@user_bp.route('/api/signup', methods=['POST'])
def signup() -> Response:
    email = request.form.get('email', type=str).lower()
    password = request.form.get('password')
    username = request.form.get('username', type=str)
    
    db = Database()
    user: User = User(db)
    result: dict[str, int | str] = user.register(email, password, username)
    if result['status'] == 200:
        return jsonify(result)
    else:
        return jsonify(result)


@user_bp .route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('login_page'))
