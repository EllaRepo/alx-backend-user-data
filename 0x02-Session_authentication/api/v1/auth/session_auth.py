#!/usr/bin/env python3
"""Session Auth Module
"""
from api.v1.auth.auth import Auth
from models.user import User
from flask import request
from typing import List, TypeVar
import base64


class SessionAuth(Auth):
    """Session Authentication class
    """
