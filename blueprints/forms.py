import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    # A form for login information

class RegisterForm(wtforms.Form):
    __tablename__ = "user"
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])
    # A form for registering information

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_mod = EmailCaptchaModel.query.filter_by(email=email).first
        if not captcha_mod and captcha_mod.lower() != captcha.lower():
            raise wtforms.ValidationError("Validation error")
        # Verification Indicates the verification code

    def validate_email(self, field):
        email = field.data
        user_mod = UserModel.query.filter_by(email=email).first()
        print("4")
        if user_mod:
            raise wtforms.ValidationError("An account with the same address already exists")
        # Verify Email entry

    def validate_username(self, field):
        username = field.data
        user_mod = UserModel.query.filter_by(username= username).first()
        if user_mod:
            raise wtforms.ValidationError("An account with the same username already exists")
        # Verify user name fill

class ForumForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])
    #Forum Form


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
    # Comment form

class ChangeForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_change = wtforms.StringField(validators=[length(min=6, max=20)])
    signature = wtforms.StringField(validators=[length(min=0, max=20)])
    # A form for modifying user information

class ChangeNameForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    # A form for modifying user names

class ChangeSignForm(wtforms.Form):
    signature = wtforms.StringField(validators=[length(min=0, max=20)])
    email = wtforms.StringField(validators=[email()])
    # A form for modifying signature

