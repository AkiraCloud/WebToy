from flask import render_template, redirect, request, flash, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from flask_sqlalchemy import get_debug_queries
from app import db
from datetime import datetime
from app.models import User, TransferInfo
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.last_login_datetime = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
