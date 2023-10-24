from flask import Blueprint, render_template, request, redirect, url_for
from .models import Experience
from . import db
from datetime import datetime
from .utils import update_experience_statuses 


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    experiences = db.session.scalars(db.select(Experience)).all()   
    current_time = datetime.now()
    update_experience_statuses()
     
    return render_template('index.html', experiences=experiences, datetime=datetime, current_time=current_time)

@bp.route('/booking-history')
def history():
    update_experience_statuses()
    return render_template('booking-history.html')



