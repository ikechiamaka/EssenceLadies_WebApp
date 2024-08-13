from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileField, FileAllowed

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class RegistrationForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(), Email(), EqualTo('email')])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    services_interested_in = StringField('Services interested In', validators=[DataRequired()])
    preferred_contact_method = SelectField('Preferred Contact Method', choices=[('Email', 'Email'), ('Phone', 'Phone')], validators=[DataRequired()])
    membership = SelectField('Membership', choices=[('Standard', 'Standard'), ('Premium', 'Premium')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')




class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    age = IntegerField('Age', validators=[Optional()])
    nationality = StringField('Nationality', validators=[Optional()])
    height = StringField('Height', validators=[Optional()])
    stats = StringField('Stats', validators=[Optional()])
    dress_size = StringField('Dress Size', validators=[Optional()])
    hair_color = StringField('Hair Color', validators=[Optional()])
    eye_color = StringField('Eye Color', validators=[Optional()])
    service_level = StringField('Service Level', validators=[Optional()])
    languages = StringField('Languages', validators=[Optional()])
    bisexual = BooleanField('Bisexual', validators=[Optional()])
    incall_location = StringField('Incall Location', validators=[Optional()])
    outcall_location = StringField('Outcall Location', validators=[Optional()])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create Profile')
