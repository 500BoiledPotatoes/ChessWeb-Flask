from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
# Table of verification codes
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    signature = db.Column(db.String(200), nullable=True)
    icon = db.Column(db.String(100))
    chess_win = db.Column(db.Integer, default=0)
    chess_lose = db.Column(db.Integer, default=0)
# Table of user info

class BookModel(db.Model):
    __tablename__='book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10))
    title = db.Column(db.String(100))
    publisher = db.Column(db.String(20))
    year = db.Column(db.Integer)
    author = db.Column(db.String(100))
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    uploader = db.relationship("UserModel",backref="book")
class ForumModel(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("UserModel", backref="forum")
    create_time = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
# Table of posts
class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey("forum.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("ForumModel",backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship("UserModel",backref="answers")

    def __str__(self):
        return self.content
# Table of comments
