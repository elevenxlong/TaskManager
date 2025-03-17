#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 20:39
# @Author  : 谢春龙
# @File    : viewsets.py
# @Software: PyCharm
# @Description:

from fastapi import Depends, HTTPException, Query, FastAPI
from typing import List
from sqlalchemy.orm import Session

from . import schemas
from . import crud
from .events import lifespan
from .settings import SessionLocal

app = FastAPI(lifespan=lifespan)


# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    print(db)
    try:
        yield db
    finally:
        db.close()


# 创建任务
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


# 获取所有任务（支持分页）
@app.get("/tasks/", response_model=List[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tasks(db, skip=skip, limit=limit)


# 获取单个任务
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# 更新任务
@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# 删除任务
@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# 按优先级或截止日期排序
@app.get("/tasks/sort/", response_model=List[schemas.Task])
def sort_tasks(sort_by: str = Query("due_date"), db: Session = Depends(get_db)):
    """
    :param sort_by:
     * due_date: 按结束日期升序
     * -deu_date: 按结束日期降序
     * priority: 按优先级升序
     * -priority: 按优先级降序
    :param db:
    """
    return crud.sort_tasks(db=db, sort_by=sort_by)


