#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/11/12 16:12
# Author  : W 
# FileName: forms.py
"""封装表单类"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,RadioField,DateField,SelectField,SubmitField
from wtforms.validators import DataRequired

"""https://www.jianshu.com/p/06bd93e21945"""
# 定义的表单都需要继承自FlaskForm
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField(u'User Name', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    rememberMe = BooleanField(u'remember me', default=False)

class MessageForm(FlaskForm):
    #学生信息填写表单
    sno = StringField('学号：',validators=[DataRequired('学号不能为空！')])
    sid = StringField('身份证号码：',validators=[DataRequired('身份证号码不能为空！')])
    sname = StringField('学生姓名：',validators=[DataRequired('姓名不能为空！')])
    ssex = RadioField('性别：',choices=[('男','男'),('女','女')],default='男')
    sbirth = DateField('出生日期：',format='%Y-%m-%d')
    sdept = SelectField('所在院系：',choices=[('人工智能学院','人工智能学院'),('机电工程学院','机电工程学院'),('电子与通信工程学院','电子与通信工程学院')])
    sspecial = SelectField('专业：',choices=[])
    sclass = StringField('班级：',validators=[DataRequired('请填入数字')])
    submit = SubmitField('确认')