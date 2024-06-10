#!/usr/bin/env python3
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from posthive.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', 
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is already taken')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    picture = FileField(
        'update Pic', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken')

    def validate_email(self, email):
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('Email address is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title',
            validators=[DataRequired()])
    content = TextAreaField('Content',
            validators=[DataRequired()])
    submit = SubmitField('Submit Post')