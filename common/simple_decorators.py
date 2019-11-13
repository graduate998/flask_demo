#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/11/12 16:20
# Author  : W 
# FileName: simple_decorators.py
"""封装装饰器"""

from flask import abort
from flask_login import current_user

#权限管理装饰器
def user_required(role):
    print("执行权限管理装饰器")
    def decorator(func):
        def wrapper(*args, **kwargs):
            """
            1.根据User.get身份
            2.身份 与 role
            :param args:
            :param kwargs:
            :return:
            """
            if current_user.rank != "1":
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator