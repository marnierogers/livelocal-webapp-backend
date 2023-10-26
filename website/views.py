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

@bp.route('/search')
def search():
    if 'search' in request.args and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        experiences = db.session.scalars(db.select(Experience).filter(Experience.name.ilike(query)))

        return render_template('index.html', experiences=experiences)
    else:
        return redirect(url_for('main.index'))
    



