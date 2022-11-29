from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
	
class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	submit = SubmitField('Register')
	
class ProfileForm(FlaskForm):
	dob = DateField ('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators = [DataRequired()])
	gender = RadioField('Gender', choices = [('0','Male'),('1','Female')], validators=[DataRequired()])
	cv = FileField('Your CV', validators = [FileAllowed(['pdf'], 'Only PDF files please')])
	submit = SubmitField('Update Profile')
	
class PostForm(FlaskForm):
	postbody = StringField('MicroPost', validators=[DataRequired()])
	submit = SubmitField('Add Post')
	
class JoinForm(FlaskForm):
	player1 = StringField('PlayerId', validators=[DataRequired()])
	player2 = StringField('PlayerId2',validators=[DataRequired()])
	submit = SubmitField('Create a match')

class ChessForm(FlaskForm):
	xy = StringField('XY',validators=[DataRequired()])
	submit = SubmitField('Confirm SUBMIT')
	
	
	



