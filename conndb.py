from flask import Flask,render_template,request,flash,Blueprint,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,RadioField,DateField,SelectField
from wtforms.validators import DataRequired
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/sducardsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wangyuting'

db=SQLAlchemy(app)
'''
1、配置数据库
2、添加学生信息、校园卡基本信息、校园卡中心、充值信息、挂失信息、餐厅信息、
   超市信息、校车信息、消费刷卡信息记录、宿舍信息、归宿刷卡信息、图书馆信息、图书馆借阅刷卡记录等模型
3、添加数据
4、使用模板显示数据库查询的数据
'''

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


@app.route('/student',methods=['GET','POST'])
def student():

    students = Student.query.all()
    return render_template('students.html',students=students,
                           columns=['学号','身份证号码','姓名','性别','出生日期','院系','专业','班级','生源地'])

@app.route('/card/<sno>',methods=['GET','POST'])
def card(sno):
    # cards = Card.query.all()
    cards = Card.query.filter_by(sno=sno)
    return render_template('card.html',cards=cards,columns=['卡号','学号','姓名','类型','状态','余额'])


class MessageForm(FlaskForm):
    sno = StringField('学号：',validators=[DataRequired('学号不能为空！')])
    sid = StringField('身份证号码：',validators=[DataRequired('身份证号码不能为空！')])
    sname = StringField('学生姓名：',validators=[DataRequired('姓名不能为空！')])
    ssex = RadioField('性别：',choices=[('男','男'),('女','女')],default='男')
    sbirth = DateField('出生日期：',format='%Y-%m-%d')
    sdept = SelectField('所在院系：',choices=[('人工智能学院','人工智能学院'),('机电工程学院','机电工程学院'),('电子与通信工程学院','电子与通信工程学院')])
    sspecial = SelectField('专业：',choices=[])
    sclass = StringField('班级：',validators=[DataRequired('请填入数字')])
    submit = SubmitField('确认')

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







if __name__ == '__main__':
    db.drop_all()
    db.create_all()

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
    db.session.add_all([s1,s2,s3,s4,s5])
    db.session.commit()

    c1 = Card(sid=s1.sid,cardstate='可用',cardmoney=340.00,sno=s1.sno)
    c2 = Card(sid=s2.sid,cardstate='可用',cardmoney=200.00,sno=s2.sno)
    c3 = Card(sid=s3.sid,cardstate='可用',cardmoney=0.00,sno=s3.sno)
    c4 = Card(sid=s4.sid,cardstate='可用',cardmoney=20.00,sno=s4.sno)
    c5 = Card(sid=s5.sid,cardstate='可用',cardmoney=18.00,sno=s5.sno)
    db.session.add_all([c1, c2, c3, c4, c5])
    db.session.commit()


    # f1 = FillInf()

    app.run(debug=True)