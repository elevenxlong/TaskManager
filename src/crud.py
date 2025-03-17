#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 19:26
# @Author  : 谢春龙
# @File    : crud.py
# @Software: PyCharm
# @Description:
from sqlalchemy.orm import Session

from . import models, schemas


# 创建任务
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 获取所有任务（支持分页）
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

# 获取单个任务
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# 更新任务
def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# 删除任务
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return db_task

# 按优先级或截止日期排序
def sort_tasks(db: Session, sort_by: str):
    if sort_by == "priority":
        return db.query(models.Task).order_by(models.Task.priority).all()
    elif sort_by == "due_date":
        return db.query(models.Task).order_by(models.Task.due_date).all()
    elif sort_by == "-priority":
        return db.query(models.Task).order_by(models.Task.priority.desc()).all()
    elif sort_by == "-due_date":
        return db.query(models.Task).order_by(models.Task.due_date.desc()).all()