from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gumshuda.models import User
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
	name = StringField('name',
	 validators = [DataRequired(), Length(min = 2, max = 25) ])
	email = StringField('email', 
		validators = [DataRequired(), Email() ])
	password = PasswordField('password', 
		validators = [DataRequired(), Length(min = 2, max = 25)])
	confirm_password = PasswordField('confirm_password', 
		validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	# Custom Validation for unique email
	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('That Email is taken, Please choose different Email ')


class LoginForm(FlaskForm):
	email = StringField('email', 
		validators = [DataRequired(), Email() ])
	password = PasswordField('password', 
		validators = [DataRequired(), Length(min = 2, max = 25)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign Up')

class addMissingPerson(FlaskForm):
	name = StringField('name',
	 validators = [DataRequired(), Length(min = 2, max = 25) ])
	age = IntegerField('age', 
		validators= [DataRequired()])
	height = IntegerField('height in feet',
		validators = [DataRequired()] )
	colour = StringField('colour of the person', 
		validators = [DataRequired(), Length(min=2, max=10)] )
	lostAt = StringField('Last seen location', 
		validators=[DataRequired(), Length(min=2, max=255)])
	reward = IntegerField('Reward')
	gender = StringField('gender', validators=[DataRequired(), Length(min=3, max=6)])
	contactNo = IntegerField('your contact number', 
		validators=[DataRequired()])
	image = FileField('Image of the missing person', validators=[FileAllowed(['jpg', 'png'])])
	state = StringField('State', validators=[DataRequired(), Length(min=1, max=50)])
	country = StringField('country', validators=[DataRequired(), Length(min=1, max=20)])
	attire = StringField('attire', validators=[DataRequired(), Length(min=1, max=100)])
	submit = SubmitField('Sign Up')
