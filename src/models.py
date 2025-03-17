#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 19:25
# @Author  : 谢春龙
# @File    : models.py
# @Software: PyCharm
# @Description:
import enum

from sqlalchemy import Column, Integer, String, DateTime

from src.settings import Base


# 定义优先级枚举
class Priority(int, enum.Enum):
    low = 0
    medium = 1
    high = 2

# 定义任务模型
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    due_date = Column(DateTime)
    priority = Column(Integer)  # 存储枚举值

