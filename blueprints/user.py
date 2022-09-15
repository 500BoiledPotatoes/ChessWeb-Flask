import random
import string

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
from datetime import datetime
from .forms import RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login")
def login():
    return render_template("login.html")


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
        print("11111")
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
        print(captcha)
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "Please enter your email first"})
