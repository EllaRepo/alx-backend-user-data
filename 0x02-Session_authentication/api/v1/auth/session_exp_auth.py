#!/usr/bin/env python3
"""Session Expiration Auth Module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class
    """
    def __init__(self):
        """Initialization
        """
        try:
            dura = int(os.getenv('SESSION_DURATION'))
        except Exception:
            dura = 0
        self.session_duration = dura

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID
        Args:
            user_id: user id
        Returns:
            session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method to return a User ID based on a Session ID
        """
        if session_id is None or type(session_id) != str or\
                session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict['user_id']

        if "created_at" not in session_dict:
            return None
        delta = timedelta(seconds=self.session_duration)
        print(session_dict['created_at'] + delta)
        if session_dict['created_at'] + delta < datetime.now():
            return None
        return session_dict['user_id']
