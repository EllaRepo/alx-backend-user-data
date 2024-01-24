#!/usr/bin/env python3
"""Test module
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

email = "ella@me.com"
password = "MyPwdOfElla"
url = "http://127.0.0.1:5000/"


def register_user(email: str, password: str) -> None:
    """Tests /users endpoint
    """
    data = {"email": email, "password": password}
    r = requests.post(url + "users", data=data)
    assert 200 == r.status_code
    assert {"email": email, "message": "user created"} == r.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password
    """
    data = {"email": email, "password": "wrong pswd"}
    r = requests.post(url + "sessions", data=data)
    assert 401 == r.status_code


def profile_unlogged() -> None:
    """Test no user profile
    """
    cookie = {"session_id": "wrong cookie"}
    r = requests.get(url + "profile", cookies=cookie)
    assert 403 == r.status_code


def log_in(email: str, password: str) -> str:
    """Test login
    """
    data = {"email": email, "password": password}
    r = requests.post(url + "sessions", data)
    cookie = r.cookies["session_id"]
    assert 200 == r.status_code
    assert isinstance(cookie, str)
    return cookie


def profile_logged(session_id: str) -> None:
    """Test logged in user
    """
    cookie = {"session_id": session_id}
    r = requests.get(url + "profile", cookies=cookie)
    assert 200 == r.status_code
    assert {"email": EMAIL} == r.json()


def log_out(session_id: str) -> None:
    """Test log_out endpoint
    """
    cookie = {"session_id": session_id}
    r = requests.delete(url + "sessions", cookies=cookie)
    assert 200 == r.status_code


def reset_password_token(email: str) -> str:
    """Test reset_password endpoint
    """
    data = {
        "email": email,
    }
    r = requests.post(url + "reset_password", data=data)
    assert 200 == r.status_code
    token = r.json()["reset_token"]
    assert len(token) == 36
    return token


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """Tests reset_password endpoint
    """
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    r = requests.put(url + "reset_password", data=data)
    assert 200 == r.status_code
    payload = r.json()
    assert payload == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
