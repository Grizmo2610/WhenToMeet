from flask import Flask, Response, render_template, redirect, url_for, request, session, jsonify

from app import *
import os

app: Flask = create_app()

@app.route('/')
def login_page() -> str:
    if 'user_id' in session:
        return redirect(url_for('main_page'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def main_page():
    return render_template('dashboard.html')

@app.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(debug=True)
    session.clear()
