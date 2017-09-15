from flask import Flask, redirect, url_for, request, session
#from flask.ext.session import Session
from flask import Flask, render_template
from flask import send_from_directory
import pymysql
pymysql.install_as_MySQLdb()
from flask.ext.bootstrap import Bootstrap
from flask import jsonify



from flask_login import LoginManager, AnonymousUserMixin, UserMixin, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os

login_manger = LoginManager()
app = Flask(__name__, static_url_path='')
#app_session = Session()
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Letmein123@localhost:3306/mydb?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

#认证加密程度
login_manger.session_protection = 'weak'

login_manger.login_view='auth.login'
#登陆提示信息
login_manger.login_message=u'对不起，您还没有登录'
login_manger.login_message_category='info'

#class Users(db.Model,UserMixin):


class NotificationRecipientList(db.Model):
    __tablename__ = 'notification_recipient_list'
    id = db.Column(db.Integer, primary_key=True)
    is_read = db.Column(db.Integer)
    notifications_id = db.Column(db.Integer, db.ForeignKey('user_notifications.id'))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class UserNotifications(db.Model):
    __tablename__ = 'user_notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(255))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notification_recipient_list = db.relationship('NotificationRecipientList', backref='user_notifications')
    created_datetime = db.Column(db.DateTime)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(64), nullable=False)

    user_notifications = db.relationship('UserNotifications', backref='user')
    notification_recipient_list = db.relationship('NotificationRecipientList', backref='user')

    def is_authenticated(self):
        """Check the user whether logged in."""
        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True


@login_manger.user_loader
def load_user(user_id):
    userobj = Users.query.filter_by(id=user_id).first()
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
    userobj = Users.query.filter_by(username=username).first()
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
        notification_recipient_list = NotificationRecipientList.query.filter_by(users_id=session['user_id'])
        # notifications = UserNotifications.query.filter_by(users_id=session['user_id'])
        return render_template('index.html', username=session['username'],
                               notification_recipient_list=notification_recipient_list)
    else:
        return render_template('login.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    login_manger.init_app(app)
    #app_session.init_app(app)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
