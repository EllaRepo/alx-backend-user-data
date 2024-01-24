#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Return a salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """Returns a uuid4 str
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Get session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets user by session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Removes user's session_id
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Updates a users reset token field
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a users password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_p = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_p,
                             reset_token=None)
