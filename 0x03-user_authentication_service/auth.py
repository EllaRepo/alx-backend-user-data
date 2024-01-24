#!/usr/bin/env python3
"""Auth module
"""
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        user_exists = False
        try:
            existing_user = self._db.find_user_by(email=email)
            user_exists = True
        except Exception:
            pass

        if user_exists:
            raise ValueError(f"User {email} already exists")

        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login is valid
        """
        try:
            user = self._db.find_user_by(email=email)
            psswd = password.encode('utf-8')
            if user and bcrypt.checkpw(psswd, user.hashed_password):
                return True
        except Exception:
            pass
        return False
