#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """ POST /auth_session/login
    Return:
      - the dictionary representation of the User
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if users is None or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        usr = users[0]
        if usr.is_valid_password(password) is False:
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        session_id = auth.create_session(usr.id)
        cookie_name = os.getenv('SESSION_NAME')

        response = jsonify(usr.to_json())

        response.set_cookie(cookie_name, session_id)

        return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout() -> str:
    """Session logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
