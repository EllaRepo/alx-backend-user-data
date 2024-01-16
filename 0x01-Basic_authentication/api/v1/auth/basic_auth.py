#!/usr/bin/env python3
"""Basic Auth Module
"""
from api.v1.auth.auth import Auth
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
