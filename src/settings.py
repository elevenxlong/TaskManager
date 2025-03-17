#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 19:26
# @Author  : 谢春龙
# @File    : settings.py
# @Software: PyCharm
# @Description:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()