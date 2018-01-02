# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, DateField, SelectField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import input_required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class TransInfoFrom(FlaskForm):
    startDate = DateTimeField('Start date', validators=[input_required(), Length(1, 64), Regexp('^(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))$|^((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[13579][26])00))-02-29)$', 0, 'Dateformat:YYYY-MM-DD')])
    endDate = DateTimeField('End date', validators=[input_required(), Length(1, 64), Regexp('^(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))$|^((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[13579][26])00))-02-29)$', 0, 'Dateformat:YYYY-MM-DD')])
    infoContent = TextAreaField('Content', validators=[input_required()])
    title = StringField('Title', validators=[input_required()])
    submit = SubmitField('Submit')
