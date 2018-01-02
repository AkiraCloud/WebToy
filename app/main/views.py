from flask import render_template, redirect, request, flash, url_for
from . import main
from flask_sqlalchemy import get_debug_queries
from app import db
from datetime import datetime
from app.models import User, TransferInfo
from flask_login import login_user, login_required, current_user
from .forms import TransInfoFrom


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TransInfoFrom()
    # if form.submit.data and form.validate_on_submit():

    if form.submit.data:
        transferInfo = TransferInfo(input_id=current_user.id,
                                    start_date=form.startDate.data,
                                    end_date=form.endDate.data,
                                    transfer_info_content=form.infoContent.data,
                                    invalid=0,
                                    title=form.title.data,
                                    owner_id=current_user.id)

        db.session.add(transferInfo)
        db.session.commit()

    trasnfer_info_list = TransferInfo.query.filter_by(input_id=current_user.id)
    return render_template('index.html', time=datetime.utcnow(), form=form, trasnfer_info_list=trasnfer_info_list)


@main.route('/user/operation', methods=['GET'])
@login_required
def operation():
    return render_template('operation.html')
