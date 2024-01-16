#!/usr/bin/env python3
"""Basic Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method for required authentication
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path_slash = path if path.endswith('/') else path + '/'
        return all(p not in path_slash for p in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Public method for handling authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method for current user handling
        """
        return None
