from flask import render_template, redirect, request, flash, url_for
from . import main
from flask_sqlalchemy import get_debug_queries
from app import db
from datetime import datetime
from app.models import User, TransferInfo
from flask_login import login_user, login_required, current_user


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', time=datetime.utcnow())


@main.route('/user/operation', methods=['GET'])
@login_required
def operation():
    return render_template('operation.html')
