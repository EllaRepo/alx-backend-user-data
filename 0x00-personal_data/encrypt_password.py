#!/usr/bin/env python3
"""Password encrypting module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.
    Args:
        password: The input password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed
