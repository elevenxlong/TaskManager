# 简易RESTful API任务管理系统

## 1. 项目概述
本项目是一个基于FastAPI框架的简易RESTful API任务管理系统，允许用户创建、查看、更新和删除任务。任务包含标题、描述、截止日期和优先级等字段，并支持按优先级或截止日期排序。

## 2. 技术栈
* 语言版本：python3.10

* 框架：FastAPI

* 数据库：SQLite

* 数据验证：Pydantic

* API文档：Swagger（FastAPI自动生成）

## 3. 项目结构
```python
TaskManager/
├── src
    ├── models.py                # 数据库模型定义
    ├── schemas.py               # Pydantic模型定义
    ├── crud.py                  # 数据库操作逻辑
    ├── settings.py              # 配置
    ├── viewsets.py              # api接口视图
    ├── events.py                # 项目启动初始化逻辑
├── tests
    ├── test_main.py                # 单元测试主逻辑
    ├── run.py                      # 单元测试启动入口
├── main.py                  # 主程序入口
├── requirements.txt         # 依赖列表
└── README.md                # 项目说明文档
```
## 4. 运行项目
a. 安装依赖：
```bash
pip install -r requirements.txt
```
b. 启动服务：
```bash
python3 main.py
```
c. 访问API文档：

* Swagger UI：http://127.0.0.1:8000/docs
* ReDoc：http://127.0.0.1:8000/redoc

## 5. 单元测试
测试覆盖主要功能

a. 启动
```bash
cd tests
python3 run.py
```

## 6. 仓库
github地址：https://github.com/elevenxlong/TaskManager/tree/master