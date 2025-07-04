#coding=utf-8
"""
# Author: Wenbing.Wang
# Created Time : 二  6/10 08:14:41 2025

# File Name: app/forms.py
# Description:

"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被使用')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被使用')

class PhotoForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述', validators=[Length(max=500)])
    photo = FileField('上传照片', validators=[DataRequired()])
    submit = SubmitField('上传')

class CommentForm(FlaskForm):
    content = TextAreaField('评论', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('提交')
