from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, session
from flask_login import login_required, current_user, login_user
from flask_sqlalchemy import get_debug_queries
#from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from . import db
from . models import Permission, Role, User, NotificationRecipientList
from . decorators import admin_required, permission_required
from .. import app
from . import login_manager
from flask import jsonify
from datetime import timedelta


@login_manager.user_loader
def load_user(user_id):
    userobj = User.query.filter_by(id=user_id).first()
    return userobj

# @app.route('/')
# def index():
#     #return render_template('index.html')
#     return app.send_static_file('index.html')

@app.route('/show_data', methods=['GET'])
def show_data():
    result = {
        'status': 'success',
        'data': 'Hello, world!',
    }
    return jsonify(result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return ''

    username = request.form.get('username')
    cookie_username = request.cookies.get('username')
    userobj = User.query.filter_by(username=username).first()
    if userobj is None:
        return render_template('login.html')

    if request.form.get('password') == userobj.password:
        login_user(userobj)
        session['username'] = request.form['username']
        # session['userobj'] = userobj
        return redirect(url_for('index'))

    return render_template('login.html')

# @app.route('/unconfirmed/')
# def unconfirmed():
#     if current_user.is_anonymous:
#         return  redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return app.send_static_file('assets/' + path)

@app.route('/')
def index():
    if 'username' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=15)
        notification_recipient_list = NotificationRecipientList.query.filter_by(users_id=session['user_id'])
        # notifications = UserNotifications.query.filter_by(users_id=session['user_id'])
        return render_template('index.html', username=session['username'],
                               notification_recipient_list=notification_recipient_list)
    else:
        return render_template('login.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)