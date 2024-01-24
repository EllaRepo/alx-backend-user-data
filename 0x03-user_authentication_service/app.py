#!/usr/bin/env python3
"""Flask app module
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handles credentials
    """
    email = request.form.get('email')
    passwd = request.form.get('password')
    if AUTH.valid_login(email, passwd) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie('session_id', session_id)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(session_id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """profile route
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """Returns a token that allows passwd reset
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    return jsonify({
        'email': email, 'reset_token': token
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
