#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 21:36
# @Author  : 谢春龙
# @File    : events.py
# @Software: PyCharm
# @Description:
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.settings import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 创建库表
    Base.metadata.create_all(bind=engine)
    yield