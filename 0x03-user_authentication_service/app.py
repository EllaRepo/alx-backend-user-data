#!/usr/bin/env python3
"""Flask app module
"""
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
