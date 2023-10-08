from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Experience, Comment
from .forms import ExperienceForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

eventbp = Blueprint('experience', __name__, url_prefix='/experiences')


@eventbp.route('/<id>')
def show(id):
    experience = db.session.scalar(db.select(Experience).where(Experience.id==id))

    # create the comment form
    form = CommentForm()    
    return render_template('experiences/show.html', experience=experience, form=form)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = ExperienceForm()
  if form.validate_on_submit():

    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    experience = Experience(name=form.name.data, description=form.description.data,
    image=db_file_path,currency=form.currency.data)

    # add the object to the db session
    db.session.add(experience)

    # commit to the database
    db.session.commit()
    flash('Successfully created experience', 'success')

    #Always end with redirect when form is valid
    return redirect(url_for('experiences.create'))
  
  return render_template('experiences/create.html', form=form)

def check_upload_file(form):
  
  #get file data from form  
  fp = form.image.data
  filename = fp.filename

  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)

  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))

  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)

  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

# @eventbp.route('/<destination>/comment', methods=['GET', 'POST'])
# @login_required
# def comment(destination):  
#     form = CommentForm()  
#     #get the destination object associated to the page and the comment
#     destination = db.session.scalar(db.select(Destination).where(Destination.id==destination))
#     if form.validate_on_submit():  
#       #read the comment from the form
#       comment = Comment(text=form.text.data, destination=destination,
#                         user=current_user) 
#       #here the back-referencing works - comment.destination is set
#       # and the link is created
#       db.session.add(comment) 
#       db.session.commit() 

#       #flashing a message which needs to be handled by the html
#       flash('Your comment has been added', 'success')  
#       # print('Your comment has been added', 'success') 
#     # using redirect sends a GET request to destination.show
#     return redirect(url_for('destination.show', id=destination.id))