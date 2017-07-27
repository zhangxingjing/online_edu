from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    password = db.Column(db.String(100),nullable=False)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    #now()获取服务器第一次运行的时间
    #now每次创建模型,获取当前时间
    create_time = db.Column(db.DATETIME,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('questions'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DATETIME, default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    question = db.relationship('Question',backref=db.backref('comments1',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('comments2'))