from common.forms import LoginForm, MessageForm
from common.simple_decorators import user_required
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  #解决编码问题
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/sducardsystem?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "wyt"    #设置token 生成salt

db=SQLAlchemy(app)

from models import User,Student,Card

# db.drop_all()
print("删除成功")
# db.create_all()
print("成功")

# use login manager to manage session 使用登录管理器管理会话
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'            #登录视图
login_manager.login_message = u"用户失效！"   #快闪消息
login_manager.init_app(app=app)

# csrf protection 开启csrf_token保护
csrf = CSRFProtect()
csrf.init_app(app)
#关闭 app.config['WTF_CSRF_ENABLED'] = False

# 这个callback函数用于reload User object，根据session中存储的user id
# 提供user_loader的回调函数，主要是通过获取user对象存储到session中，自己实现最好启用缓存
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/student',methods=['GET','POST'])
def student():
    students = Student.query.all()
    # print(type(students))
    return render_template('students.html',students=students,
                           columns=['学号','身份证号码','姓名','性别','出生日期','院系','专业','班级','生源地'])

@app.route('/card/<sno>',methods=['GET','POST'])
def card(sno):
    # cards = Card.query.all()
    cards = Card.query.filter_by(sno=sno)
    return render_template('card.html',cards=cards,columns=['卡号','学号','姓名','类型','状态','余额'])

@app.route('/add_student',methods=['POST','GET'])
def add_student():
    student_form = MessageForm()
    if student_form.validate_on_submit():
        sno = student_form.sno.data
        sid = student_form.sid.data
        sname = student_form.sname.data
        ssex = student_form.ssex.data
        sbrith = student_form.sbirth.data
        sdept = student_form.sdept.data
        sclass = student_form.sclass.data
        student = Student.query.filter_by(sno=sno).first()
        if sno:
            sno = Card.query.filter_by(sno=student.sno).first()
            if sno:
                flash('该学生信息已存在')
        else:
            try:
                new_student = Student(sno=student.sno,sid=sid,sname=sname,ssex=ssex,sbirth=sbrith,sdept=sdept,sclass=sclass)
                db.session.add(new_student)
                db.session.commit()
                flash('该学生信息已添加')
            except Exception as e:
                print(e)
                flash('学生信息添加失败')
                db.session.rollback()
    else:
        if request.method == 'POST':
            flash('参数不全')

    return render_template('student_message.html',form=student_form)

# app.py
@app.route('/')
@app.route('/login',methods=["GET","POST"])
def login():
    print("进来登录了")
    form = LoginForm()
    if form.validate_on_submit():
        print("进来这个函数了")
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        print(user_name,password)
        user = User(user_name)
        if user.verify_password(password):
            print("进来储存用户啦")
            print(user.username,user.id)
            login_user(user, remember=remember_me)
            print("zheyibu")
            return redirect(url_for('main'))
        flash(u"用户名或密码错误！")
    return render_template('login.html', title="Sign In", form=form)

@app.route('/main')
@login_required
def main():
    return render_template(
        'index.html', username=current_user.username)

@app.route('/logout',endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

"""
gunicorn启动报错可以增加-preload查看详细报错信息
flask要求您将单个“视图函数”与“端点”关联起来，调用两次装饰器，
这将创建两个不同的函数(功能完全相同，但内存签名不同)。
所以解决的方法如下：
在每个使用装饰器的的路由上，使用断点。
endpoint=
https://blog.csdn.net/ybw_2569/article/details/98885222"""
@app.route('/crud',endpoint="crud")
@login_required
# @user_required
def crud():
    return render_template(
        'crud.html', username=current_user.username)

@app.route("/getlist", endpoint="getList",methods=["GET","POST"])
@login_required
# @user_required
def getList():
    student = Student.query.all()
    infolist = []
    for i in student:
        temdict = {}
        temdict["no"] = i.sno
        temdict["id"] = i.sid
        temdict["name"] = i.sname
        temdict["sex"] = i.ssex
        temdict["birth"] = str(i.sbirth)
        # print(type(i.sbirth))
        # print(str(i.sbirth))
        temdict["dept"] = i.sdept
        temdict["special"] = i.sspecial
        temdict["class"] = i.sclass
        infolist.append(temdict)
#     infolist = [
#     {
#         "id": 1,
#         "username": "shuzheng",
#         "password": "123456",
#         "name": "555555555",
#         "sex": 1,
#         "age": 28,
#         "phone": 13987654321,
#         "email": "469741414@qq.com",
#         "address": "中国 北京",
#         "remark": "官网：http://www.shuzheng.cn"
#     },
#     {
#         "id": 2,
#         "username": "shuzheng",
#         "password": "123456",
#         "name": "666666666666",
#         "sex": 1,
#         "age": 28,
#         "phone": 13987654321,
#         "email": "469741414@qq.com",
#         "address": "中国 北京",
#         "remark": "官网：http://www.shuzheng.cn"
#     }
# ]
    # json_infolist = json.dumps(infolist,ensure_ascii=False)
    return jsonify(infolist)

@app.route("/temrunadd")
def temrunadd():
    s1 = Student(sno='17240130', sid='44058319990123042X', sname='王钰婷', ssex='女', sbirth='1999-01-23',
                 sdept='人工智能学院', sspecial='计算机信息管理', sclass='4班', saddr='广东省汕头市澄海区')
    s2 = Student(sno='17240224', sid='440111199803073156', sname='曾禹祥', ssex='男', sbirth='1998-03-07',
                 sdept='人工智能学院', sspecial='计算机信息管理', sclass='2班', saddr='广东省广州市白云区')
    s3 = Student(sno='17140143', sid='440304199810266877', sname='陈逸轩', ssex='男', sbirth='1998-10-26',
                 sdept='电子与通信工程学院', sspecial='电子信息工程技术', sclass='1班', saddr='广东省深圳市福田区')
    s4 = Student(sno='17340111', sid='444522419981111607', sname='李晓璇', ssex='女', sbirth='1998-11-11',
                 sdept='建筑与环境工程学院', sspecial='房地产经营与管理', sclass='3班', saddr='广东省揭阳市惠来县')
    s5 = Student(sno='17440134', sid='440306199902024130', sname='许奕涵', ssex='男', sbirth='1999-02-02',
                 sdept='机电工程学院', sspecial='建筑智能化工程技术', sclass='2班', saddr='广东省深圳市宝安区')
    db.session.add_all([s1, s2, s3, s4, s5])
    db.session.commit()

    c1 = Card(sid=s1.sid, cardstate='可用', cardmoney=340.00, sno=s1.sno)
    c2 = Card(sid=s2.sid, cardstate='可用', cardmoney=200.00, sno=s2.sno)
    c3 = Card(sid=s3.sid, cardstate='可用', cardmoney=0.00, sno=s3.sno)
    c4 = Card(sid=s4.sid, cardstate='可用', cardmoney=20.00, sno=s4.sno)
    c5 = Card(sid=s5.sid, cardstate='可用', cardmoney=18.00, sno=s5.sno)
    db.session.add_all([c1, c2, c3, c4, c5])
    db.session.commit()
    print("添加成功")

if __name__ == '__main__':
    # s1 = Student(sno='17240130', sid='44058319990123042X', sname='王钰婷', ssex='女', sbirth='1999-01-23',
    #              sdept='人工智能学院', sspecial='计算机信息管理', sclass='4班', saddr='广东省汕头市澄海区')
    # s2 = Student(sno='17240224', sid='440111199803073156', sname='曾禹祥', ssex='男', sbirth='1998-03-07',
    #              sdept='人工智能学院', sspecial='计算机信息管理', sclass='2班', saddr='广东省广州市白云区')
    # s3 = Student(sno='17140143', sid='440304199810266877', sname='陈逸轩', ssex='男', sbirth='1998-10-26',
    #              sdept='电子与通信工程学院', sspecial='电子信息工程技术', sclass='1班', saddr='广东省深圳市福田区')
    # s4 = Student(sno='17340111', sid='444522419981111607', sname='李晓璇', ssex='女', sbirth='1998-11-11',
    #              sdept='建筑与环境工程学院', sspecial='房地产经营与管理', sclass='3班', saddr='广东省揭阳市惠来县')
    # s5 = Student(sno='17440134', sid='440306199902024130', sname='许奕涵', ssex='男', sbirth='1999-02-02',
    #              sdept='机电工程学院', sspecial='建筑智能化工程技术', sclass='2班', saddr='广东省深圳市宝安区')
    # db.session.add_all([s1, s2, s3, s4, s5])
    # db.session.commit()
    #
    # c1 = Card(sid=s1.sid, cardstate='可用', cardmoney=340.00, sno=s1.sno)
    # c2 = Card(sid=s2.sid, cardstate='可用', cardmoney=200.00, sno=s2.sno)
    # c3 = Card(sid=s3.sid, cardstate='可用', cardmoney=0.00, sno=s3.sno)
    # c4 = Card(sid=s4.sid, cardstate='可用', cardmoney=20.00, sno=s4.sno)
    # c5 = Card(sid=s5.sid, cardstate='可用', cardmoney=18.00, sno=s5.sno)
    # db.session.add_all([c1, c2, c3, c4, c5])
    # db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=5000)
