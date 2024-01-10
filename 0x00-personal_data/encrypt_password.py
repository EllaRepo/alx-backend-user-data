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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password.
    Args:
        hashed_password: The hashed password as a byte string.
        password: The input password to be validated.
    Returns:
        bool: True if the password matches the hashed password, False otherwise
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
