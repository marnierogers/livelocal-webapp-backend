from flask import Blueprint, render_template, request, redirect, url_for
from .models import Experience
from . import db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    experiences = db.session.scalars(db.select(Experience)).all()    
    return render_template('index.html', experiences=experiences, datetime=datetime)

@bp.route('/booking-history')
def history():
    return render_template('booking-history.html')



