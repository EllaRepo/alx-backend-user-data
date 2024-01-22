#!/usr/bin/env python3
"""Module define User Model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model class
    """
    __tablename__ = 'users'

    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
    session_id: Column = Column(String, nullable=True)
    reset_token: Column = Column(String, nullable=True)
