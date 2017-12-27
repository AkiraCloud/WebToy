from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import input_required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[input_required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[input_required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[input_required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        input_required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        input_required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[input_required()])
    submit = SubmitField('Register')
