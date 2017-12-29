

# -*- coding:utf-8 -*-
from datetime import datetime
import hashlib
from app import db,login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.exceptions import ValidationError

class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    last_login_datetime = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))
    transfer_info_relationship = db.relationship('TransferInfo', backref='user', foreign_keys="[TransferInfo.input_id]")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'email': self.email,
            'password': self.password_hash
        }
        return json_user

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class TransferInfo(db.Model):
    __tablename__ = 'transferinfo'
    id = db.Column(db.Integer, primary_key=True)
    input_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.DateTime(), default=datetime.utcnow())
    end_date = db.Column(db.DateTime(), default=datetime.utcnow())
    title = db.Column(db.String(64))
    transfer_info_content = db.Column(db.Text)
    invalid = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def get_effect(self):
        pass
        

    def to_json(self):
        json_transferinfo = {
            'input_id': self.input_id,
            'start_date' : self.start_date,
            'end_date': self.end_date,
            'transfer_info_content': self.transfer_info_content,
            'invalid_or_not': self.invalid
        }
        return json_transferinfo

