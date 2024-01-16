#!/usr/bin/env python3
"""Basic Auth Module
"""
from api.v1.auth.auth import Auth
from models.user import User
from flask import request
from typing import List, TypeVar
import base64


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """Basic - Base64 part
        """
        if authorization_header is None or not\
            isinstance(authorization_header, str) or\
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Basic - Base64 decode
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            de = base64.b64decode(base64_authorization_header).decode('utf-8')
            return de
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Basic - User credentials
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        colon_index = decoded_base64_authorization_header.index(':')
        email = decoded_base64_authorization_header[:colon_index]
        password = decoded_base64_authorization_header[colon_index + 1:]
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Basic - User object
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        User.load_from_file()
        count = User.count()
        if not count:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Basic - Overload current_user
        """
        auth_header = self.authorization_header(request)
        credential = self.extract_base64_authorization_header(auth_header)
        plain_credential = self.decode_base64_authorization_header(credential)
        email, passwd = self.extract_user_credentials(plain_credential)
        user = self.user_object_from_credentials(email, passwd)
        print(user)
        return user
