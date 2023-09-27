from flask import Blueprint, render_template, request, redirect, url_for
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/event')
def event():
    return render_template('event.html')
