#coding=utf-8
"""
# Author: Wenbing.Wang
# Created Time : 二  6/10 08:14:05 2025

# File Name: app/routes.py
# Description:

"""

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, db
from app.models import User, Photo, Comment
from app.forms import LoginForm, RegistrationForm, PhotoForm, CommentForm
import os
from PIL import Image

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.order_by(Photo.created_at.desc()).paginate(page=page, per_page=9)
    return render_template('index.html', photos=photos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已成功注册！')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        file = form.photo.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 保存原始图片
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 创建缩略图
            img = Image.open(filepath)
            img.thumbnail((800, 800))
            thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumb_' + filename)
            img.save(thumbnail_path)

            # 保存到数据库
            photo = Photo(
                title=form.title.data,
                description=form.description.data,
                filename=filename,
                author=current_user
            )
            db.session.add(photo)
            db.session.commit()
            flash('您的照片已成功上传！')
            return redirect(url_for('index'))
        else:
            flash('不支持的文件类型')
    return render_template('upload.html', title='上传照片', form=form)

@app.route('/photo/<int:photo_id>', methods=['GET', 'POST'])
def photo_detail(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('请先登录以发表评论')
            return redirect(url_for('login'))

        comment = Comment(
            content=form.content.data,
            author=current_user,
            photo=photo
        )
        db.session.add(comment)
        db.session.commit()
        flash('您的评论已发布')
        return redirect(url_for('photo_detail', photo_id=photo_id))

    return render_template('photo_detail.html', photo=photo, form=form)

@app.route('/reply/<int:comment_id>', methods=['POST'])
@login_required
def reply_comment(comment_id):
    parent_comment = Comment.query.get_or_404(comment_id)
    form = CommentForm()

    if form.validate_on_submit():
        reply = Comment(
            content=form.content.data,
            author=current_user,
            photo=parent_comment.photo,
            parent=parent_comment
        )
        db.session.add(reply)
        db.session.commit()
        flash('您的回复已发布')

    return redirect(url_for('photo_detail', photo_id=parent_comment.photo_id))

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    photos = Photo.query.filter_by(user_id=user.id).order_by(Photo.created_at.desc()).limit(12).all()
    return render_template('profile.html', user=user, photos=photos)

