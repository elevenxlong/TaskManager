#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2025/3/17 20:00
# @Author  : 谢春龙
# @File    : run.py
# @Software: PyCharm
# @Description:
import pytest


if __name__ == '__main__':
    pytest.main(['--cov=src', '-v'])