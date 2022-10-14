import random
import string

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session,flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, ForumModel
from datetime import datetime
from .forms import RegisterForm, LoginForm, ChangeForm, ChangeNameForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")

            else:
                flash("The email and password do not match")
                return redirect(url_for("user.login"))
        else:
            flash("The email and password formats are incorrect")
            return redirect(url_for("user.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))

        else:
            return redirect(url_for("user.register"))
    else:
        return render_template("register.html")


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="Mail test",
            recipients=[email],
            body=f"[WeChess] "
                 f"Your registration verification code is: {captcha}",
        )
        mail.send(message)
        captcha_mod = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_mod:
            captcha_mod.captcha = captcha
            captcha_mod.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_mod = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_mod)
            db.session.commit()
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "Please enter your email first"})

@bp.route("/change", methods=['POST','GET'])
def user_change():
    if request.method == 'POST':
        form = ChangeForm(request.form)
        form_name = ChangeNameForm(request.form)
        if form_name.validate():
            if form.validate():
                email = form.email.data
                username = form.username.data
                password = form.password.data
                hash_password = generate_password_hash(password)
                user = UserModel.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    UserModel.query.filter_by(email=email).update({'password': hash_password})
                    UserModel.query.filter_by(email=email).update({'username': username})
                db.session.commit()
                flash("Change success")
                return redirect(url_for("user.centre", user_id=user.id))
            else:
                email = form.email.data
                username = form.username.data
                user = UserModel.query.filter_by(email=email).first()

                if user:
                    UserModel.query.filter_by(email=email).update({'username': username})
                    db.session.commit()
                print(user.id)
                return redirect(url_for("user.centre", user_id = user.id))
    else:
        form = ChangeForm(request.form)
        email = form.email.data
        user = UserModel.query.filter_by(email=email).first()
        return render_template("personalspace.html",user_id = user.id)


@bp.route("/centre/<int:user_id>")
def centre(user_id):
    information = UserModel.query.get(user_id)
    return render_template("personalspace.html", information=information)

@bp.route("/blog/<int:author_id>", methods=['POST','GET'])
def blog_personal(author_id):
    print(author_id)
    information = UserModel.query.get(author_id)
    questions = ForumModel.query.filter(ForumModel.author_id==author_id)
    print(questions)
    return render_template("personalblog.html", questions=questions, information=information)

