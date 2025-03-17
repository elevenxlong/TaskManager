#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 19:26
# @Author  : 谢春龙
# @File    : schemas.py
# @Software: PyCharm
# @Description:
from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# 定义优先级枚举
class Priority(int, Enum):
    low = 0
    medium = 1
    high = 2

# 定义任务创建模型
class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: Priority

# 定义任务更新模型
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None

# 定义任务响应模型
class Task(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    priority: Priority

    class Config:
        from_attributes = True