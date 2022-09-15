import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel


class RegisterForm(wtforms.Form):
    __tablename__ = "user"
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_mod = EmailCaptchaModel.query.filter_by(email=email).first
        if not captcha_mod and captcha_mod.lower() != captcha.lower():
            raise wtforms.ValidationError("Validation error")

    def validate_email(self, field):
        email = field.data
        user_mod = UserModel.query.filter_by(email=email).first()
        print("4")
        if user_mod:
            raise wtforms.ValidationError("An account with the same address already exists")

    def validate_username(self, field):
        username = field.data
        user_mod = UserModel.query.filter_by(username= username).first()
        print("5")
        if user_mod:
            raise wtforms.ValidationError("An account with the same username already exists")
