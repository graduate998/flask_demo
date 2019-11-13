#!/usr/bin/env python
# _*_coding:utf-8 _*_
# Time    : 2019/11/12 16:14
# Author  : W 
# FileName: models.py
"""封装model类"""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_login._compat import unicode
import json
import uuid
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


"""暂时测试写死用户信息文件，保存用户名和密码"""
PROFILE_FILE = "profiles.json"

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash,
                                       self.id]
            f.write(json.dumps(profiles))

    def verify_password(self, password):
        password_hash = self.get_password_hash()
        if password_hash is None:
            return False
        # return check_password_hash(self.password_hash, password)
        if password == password_hash:
            return True
        return False

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    print("校验user_info密码%s" % user_info)
                    return user_info
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        print("用户名存在，返回用户id%s" % user_profiles[self.username][1])
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None

class Student(db.Model):
    __tablename__ = 'students'
    sno = db.Column(db.String(8),primary_key=True)
    sid = db.Column(db.String(18),unique=True,nullable=False)
    sname = db.Column(db.String(20),unique=True,nullable=False)
    ssex = db.Column(db.String(4),nullable=False,default='未知')
    sbirth = db.Column(db.Date,nullable=False)
    sdept = db.Column(db.String(30),nullable=False)
    sspecial = db.Column(db.String(30),nullable=False)
    sclass = db.Column(db.String(30),nullable=False)
    saddr = db.Column(db.String(60),nullable=False)
    # cfl = db.relationship('Card','FillInf','LosInf',backref='student')
    card = db.relationship('Card',backref='student')
    fillinf = db.relationship('FillInf',backref='student')
    losinf = db.relationship('LosInf',backref='student')

class Card(db.Model):
    __tablename__ = 'cards'
    cardno = db.Column(db.Integer,primary_key=True)
    sid = db.Column(db.String(18),nullable=False)
    # cardstyle = db.Column(db.String(10),nullable=False)
    cardstate = db.Column(db.String(10),default='不可用',nullable=False)
    cardmoney = db.Column(db.Float,default=0.00,nullable=False)
    # cardtime = db.Column(db.Time,nullable=False)
    sno = db.Column(db.String(8),db.ForeignKey('students.sno'))
    # fl = db.relationship('FillInf','LosInf',backref='card')
    fillinf = db.relationship('FillInf',backref='card')
    losinf = db.relationship('LosInf',backref='card')

# class CardCenter(db.Model):
#     __tablename__ = 'cardcenter'
#     ccno = db.Column(db.String(10),primary_key=True)
#     ccaddr = db.Column(db.String(50),nullable=False)
#     jbr = db.Column(db.String(10),nullable=False)

class FillInf(db.Model):
    __tablename__ = 'fillinf'
    czno = db.Column(db.Integer,primary_key=True)
    czrq = db.Column(db.Time,nullable=False)
    czje = db.Column(db.Integer,nullable=False)
    # jbr = db.Column(db.String(10),nullable=False)
    cardno = db.Column(db.Integer,db.ForeignKey('cards.cardno'))
    sno = db.Column(db.String(8),db.ForeignKey('students.sno'))

class LosInf(db.Model):
    __tablename__ = 'losinf'
    gsno = db.Column(db.Integer,primary_key=True)
    gsrq = db.Column(db.Time,nullable=False)
    jgrq = db.Column(db.Time,nullable=False)
    # jbr = db.Column(db.String(10),nullable=False)
    cardno = db.Column(db.Integer, db.ForeignKey('cards.cardno'))
    sno = db.Column(db.String(8), db.ForeignKey('students.sno'))

