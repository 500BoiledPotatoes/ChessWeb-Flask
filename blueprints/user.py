import os
import random
import string

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, current_app
from sqlalchemy import or_

from config import Config
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
                # Verify that the username and password match
                session['user_id'] = user.id
                session['USERNAME'] = user.username
                return redirect("/play")
            # After the verification is successful, the main screen is displayed

            else:
                flash("The email and password do not match")
                return redirect(url_for("user.login"))
            # Password error redirects to log in screen
        else:
            flash("The email and password formats are incorrect")
            return redirect(url_for("user.login"))


# The realization of the login function


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('user.login'))


# User logout


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)
            # Hash encryption of passwords
            try:
                user = UserModel(email=email, username=username, password=hash_password)
                db.session.add(user)
                # Load the user information into the database
                db.session.commit()
                current_app.logger.info("Successfully register")
            except Exception as e:
                current_app.logger.debug("Failed to add user to the database", e)
                db.session.rollback()
            return redirect(url_for("user.login"))

        else:
            return redirect(url_for("user.register"))
    else:
        return render_template("register.html")


# Implementation of registration function

@bp.route("/captcha", methods=['POST'])
def get_captcha():
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="Verification code",
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
    # Each new captcha is updated in the database
    else:
        return jsonify({"code": 400, "message": "Please enter your email first"})


# Email verification code
@bp.route("/change", methods=['POST', 'GET'])
def user_change():
    if request.method == 'POST':
        form = ChangeForm(request.form)
        form_name = ChangeNameForm(request.form)
        if form_name.validate():
            if form.validate():
                email = form.email.data
                username = form.username.data
                password = form.password.data
                signature = form.signature.data
                hash_password = generate_password_hash(password)
                user = UserModel.query.filter_by(email=email).first()
                try:
                    if user and check_password_hash(user.password, password):
                        UserModel.query.filter_by(email=email).update({'password': hash_password})
                        UserModel.query.filter_by(email=email).update({'username': username})
                    if user:
                        UserModel.query.filter_by(email=email).update({'signature': signature})
                    db.session.commit()
                    flash("Change success")
                    current_app.logger.info("Successfully change")
                except Exception as e:
                    current_app.logger.debug("Database change data failure", e)
                    db.session.rollback()
                return redirect(url_for("user.centre", user_id=user.id))
            # To change the password, enter the correct old password

            else:
                email = form.email.data
                username = form.username.data
                sign = form.signature.data
                user = UserModel.query.filter_by(email=email).first()
                try:
                    if user:
                        UserModel.query.filter_by(email=email).update({'username': username})
                        UserModel.query.filter_by(email=email).update({'signature': sign})
                        db.session.commit()
                except Exception as e:
                    current_app.logger.debug("Database change data failure", e)
                    db.session.rollback()
                return redirect(url_for("user.centre", user_id=user.id))
            # Only the username is changed
    else:
        form = ChangeForm(request.form)
        email = form.email.data
        user = UserModel.query.filter_by(email=email).first()
        return render_template("personalspace.html", user_id=user.id)


# Change a user's personal information


@bp.route("/centre/<int:user_id>")
def centre(user_id):
    information = UserModel.query.get(user_id)
    return render_template("personalspace.html", information=information)
    current_app.logger.info("Successfully query user")
# Displays basic user information


@bp.route("/blog/<int:author_id>", methods=['POST', 'GET'])
def blog_personal(author_id):
    information = UserModel.query.get(author_id)
    questions = ForumModel.query.filter(ForumModel.author_id == author_id)
    current_app.logger.info("Successfully query blog_personal")
    return render_template("personalblog.html", questions=questions, information=information)


# Displays posts by the current user

@bp.route("/search/<int:author_id>")
def search(author_id):
    q = request.args.get("q")
    information = UserModel.query.get(author_id)
    questions = ForumModel.query.filter(or_(ForumModel.title.contains(q), ForumModel.content.contains(q))).order_by(
        db.text("-create_time"))
    current_app.logger.info("Successfully search book")
    return render_template("personalblog.html", questions=questions, information=information)

# Search for posts by keyword
@bp.route('/navigation/<int:user_id>')
def navigation(user_id):
    information = UserModel.query.get(user_id)
    return render_template('dashboard.html', information=information)
# dashboard navigation
