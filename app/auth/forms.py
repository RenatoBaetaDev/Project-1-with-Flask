from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.fields.html5 import EmailField

from app.models import User, Role

class RoleRegistrationForm(FlaskForm):
    name = StringField('Role', validators=[
        DataRequired()
    ])
    submit = SubmitField('Register')

    def validate_name(self, field):
        if Role.query.filter_by(name=field.data).first():
            raise ValidationError('Role already registered.')

class RegistrationForm(FlaskForm):
    username = StringField('Nickname', validators=[
        DataRequired(), Length(1, 64)
    ])
    email = EmailField('Email Address', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already used.")



class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')