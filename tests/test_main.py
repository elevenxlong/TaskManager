#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 19:57
# @Author  : 谢春龙
# @File    : test_main.py
# @Software: PyCharm
# @Description:
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.viewsets import app, get_db
from src.models import Task
from src.settings import Base

# 配置测试数据库
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 使用静态连接池
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# 依赖项：获取数据库会话
def overwrite_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建 FastAPI 的 TestClient
app.dependency_overrides[get_db] = overwrite_db
client = TestClient(app)


# 在每个测试之前清空数据库
@pytest.fixture
def clear_db():
    db = TestingSessionLocal()
    try:
        db.query(Task).delete()
        db.commit()
    finally:
        db.close()


def test_create_task(clear_db):
    # 测试数据
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2023-12-31T23:59:59",
        "priority": 1,
    }

    # 发送 POST 请求
    response = client.post("/tasks/", json=task_data)

    # 验证响应状态码和数据
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "This is a test task"
    assert response.json()["priority"] == 1


def test_get_tasks(clear_db):
    # 创建测试任务
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2023-12-31T23:59:59",
        "priority": 1,
    }
    client.post("/tasks/", json=task_data)

    # 发送 GET 请求
    response = client.get("/tasks/")

    # 验证响应状态码和数据
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"


def test_get_single_task(clear_db):
    # 测试获取单个任务功能
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2023-12-31T23:59:59",
        "priority": 1,
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # 发送 GET 请求
    response = client.get(f"/tasks/{task_id}")

    # 验证响应状态码和数据
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Test Task"

    # 测试请求不存在任务
    response = client.get(f"/tasks/99")

    # 验证响应状态码和数据
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


def test_update_task(clear_db):
    # 创建测试任务
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2023-12-31T23:59:59",
        "priority": 1,
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # 更新任务
    update_data = {"title": "Updated Task"}
    response = client.put(f"/tasks/{task_id}", json=update_data)

    # 验证响应状态码和数据
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

    # 测试更新不存在任务
    # 更新任务
    update_data = {"title": "Updated Task"}
    response = client.put(f"/tasks/99", json=update_data)

    # 验证响应状态码和数据
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


def test_delete_task(clear_db):
    # 创建测试任务
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2023-12-31T23:59:59",
        "priority": 1,
    }
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # 删除任务
    response = client.delete(f"/tasks/{task_id}")

    # 验证响应状态码和数据
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # 验证任务是否已删除
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

    # 测试删除不存在任务
    # 删除任务
    response = client.delete(f"/tasks/99")

    # 验证响应状态码和数据
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


def test_sort_tasks(clear_db):
    # 创建多个测试任务
    tasks = [
        {"title": "Task 1", "description": "Task 1", "due_date": "2023-12-31T23:59:59", "priority": 1},
        {"title": "Task 2", "description": "Task 2", "due_date": "2023-11-30T23:59:59", "priority": 2},
        {"title": "Task 3", "description": "Task 3", "due_date": "2023-10-31T23:59:59", "priority": 0},
    ]
    for task in tasks:
        client.post("/tasks/", json=task)

    # 按优先级排序
    response = client.get("/tasks/sort/?sort_by=-priority")
    assert response.status_code == 200
    priorities = [task["priority"] for task in response.json()]
    assert priorities == [2, 1, 0]  # 降序排序

    response = client.get("/tasks/sort/?sort_by=priority")
    assert response.status_code == 200
    priorities = [task["priority"] for task in response.json()]
    assert priorities == [0, 1, 2]  # 升序排序


    # 按截止日期排序
    response = client.get("/tasks/sort/?sort_by=due_date")
    assert response.status_code == 200
    due_dates = [task["due_date"] for task in response.json()]
    assert due_dates == ["2023-10-31T23:59:59", "2023-11-30T23:59:59", "2023-12-31T23:59:59"]  # 升序排序

    response = client.get("/tasks/sort/?sort_by=-due_date")
    assert response.status_code == 200
    due_dates = [task["due_date"] for task in response.json()]
    assert due_dates == ["2023-12-31T23:59:59", "2023-11-30T23:59:59", "2023-10-31T23:59:59"]  # 降序排序
