from flask import Blueprint, Response, redirect, url_for, request, session, jsonify
from app.models import User, Database

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp .route('/api/login', methods=['POST'])
def login() -> Response:
    email: str | None = request.form.get('email', type=str)
    password: str | None = request.form.get('password')
    db = Database()
    user: User = User(db)
    
    user_data = user.login(email, password)
    if user_data:
        session.permanent = True
        session['user_id'] = user_data['id']
        session['username'] = user_data['username']
        return jsonify({'status': 200, 'message': 'Login successful', 'user': user_data})
    else:
        return jsonify({'status': 401, 'message': 'Invalid credentials'})


@user_bp .route('/api/signup', methods=['POST'])
def signup() -> Response:
    email = request.form.get('email', type=str)
    password = request.form.get('password')
    if not email or not password:
        return jsonify({'status': 400, 'message': 'Missing email or password'})
    
    db = Database()
    user: User = User(db)
    success = user.register(email, password)
    if success:
        return jsonify({'status': 200, 'message': 'Registration successful'})
    else:
        return jsonify({'status': 409, 'message': 'Email already exists'})


@user_bp .route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('login_page'))
