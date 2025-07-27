from flask import Flask, Response, render_template, redirect, url_for, request, session, jsonify

from werkzeug.wrappers.response import Response
from app import create_app
from app.routes import *

import os

app: Flask = create_app()


@app.route('/')
def login_page() -> str:
    return render_template('login.html')
@app.route('/dashboard')
def main_page():
    return render_template('dashboard.html')

@app.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(debug=True)
