from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import Experience, Comment, Booking
from .forms import ExperienceForm, CommentForm, TicketSelectorForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from datetime import datetime
from .models import User



eventbp = Blueprint('experience', __name__, url_prefix='/experiences')


@eventbp.route('/<id>')
def show(id):
    experience = db.session.scalar(db.select(Experience).where(Experience.id==id))

    print(experience)
    
    # create the comment form
    form = CommentForm()  
    ticket_selector_form = TicketSelectorForm()  
    return render_template('experiences/show.html', experience=experience, form=form, ticket_selector_form=ticket_selector_form)


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = ExperienceForm()
  experience = None  # Set experience to None by default
  
  if form.validate_on_submit():

    type = form.type.data
    name = form.name.data
    description = form.description.data
    address_line1 = form.address_line1.data
    suburb = form.suburb.data
    postcode = form.postcode.data
    start_date = form.start_date.data
    start_time = form.start_time.data
    end_time = form.end_time.data
    ticket_qty = form.ticket_qty.data
    price = form.price.data
    image_1 = form.image_1.data
    image_2 = form.image_2.data
    image_3 = form.image_3.data

    # Adjust start and end time
    new_start_time = datetime.combine(start_date, start_time)
    new_end_time = datetime.combine(start_date, end_time)


    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    db_file_path_2 = check_upload_file_2(form)
    db_file_path_3 = check_upload_file_3(form)
    
    experience = Experience(type=type, name=name, description=description, address_line1=address_line1, suburb=suburb, postcode=postcode, start_date=start_date, start_time=new_start_time, end_time=new_end_time, ticket_qty=ticket_qty, price=price,
                            image_1=db_file_path, image_2=db_file_path_2, image_3=db_file_path_3, user=current_user)

    # add the object to the db session
    db.session.add(experience)

    # commit to the database
    db.session.commit()
    flash('Experience successfully created.', 'success')

    #Always end with redirect when form is valid
    return redirect(url_for('experience.create'))
  
  return render_template('experiences/create.html', form=form, experience=experience)


@eventbp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    print('Method type: ', request.method)

    # Get the currently logged-in user
    global current_user

    # Query the database to get experiences associated with the current user
    experiences = Experience.query.filter_by(user_id=current_user.id).all()

    return render_template('experiences/update.html', experiences=experiences)


@eventbp.route('/update_page/<int:experience_id>', methods=['GET', 'POST'])
@login_required
def update_page(experience_id):
    print('Method type: ', request.method)

    # Get the experience object by id and check if it belongs to the current user
    experience = Experience.query.get(experience_id)
    # Pass the experience object to the form constructor
    form = ExperienceForm(obj=experience)

    if form.validate_on_submit():
        # Update the experience object with the new form data
        form.populate_obj(experience)
        # No need to call db.session.add(experience) since it is already in the session
        db.session.commit()
        flash('Experience successfully updated.',
              'success')  # Update flash message
        return redirect(url_for('experiences.update_page'))

    return render_template('experiences/update_page.html', form=form, experience=experience)


@eventbp.route('/cancel_event/<int:experience_id>', methods=['POST'])
def cancel_event(experience_id):

    # Find the experience by ID
    experience = Experience.query.get(experience_id)

    print(experience)

    if experience:
        # Update the status to "Cancelled"
        experience.status = "Cancelled"
        db.session.commit()

    return redirect(url_for('experience.update'))


def check_upload_file(form):
  
  #get file data from form  
  fp = form.image_1.data
  filename = fp.filename

  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)

  #upload file location – directory of this file/static/image
  upload_path = os.path.join(
      BASE_PATH, 'static/img/uploads/', secure_filename(filename))

  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/uploads/' + secure_filename(filename)

  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

def check_upload_file_2(form):
  
  #get file data from form  
  fp = form.image_2.data
  filename = fp.filename

  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)

  #upload file location – directory of this file/static/image
  upload_path = os.path.join(
      BASE_PATH, 'static/img/uploads/', secure_filename(filename))

  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/uploads/' + secure_filename(filename)

  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

def check_upload_file_3(form):

  #get file data from form
  fp = form.image_3.data
  filename = fp.filename

  #get the current path of the module file… store image file relative to this path
  BASE_PATH = os.path.dirname(__file__)

  #upload file location – directory of this file/static/image
  upload_path = os.path.join(
      BASE_PATH, 'static/img/uploads/', secure_filename(filename))

  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/uploads/' + secure_filename(filename)

  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path


@eventbp.route('/<int:experience_id>/comment', methods=['GET', 'POST'])
@login_required
def comment(experience_id):

    form = CommentForm(request.form)

    print("Form data received:")
    print("Comment text:", form.text.data)
    print("Experience ID:", experience_id)

    #get the experience object associated to the page and the comment
    experience = db.session.scalar(db.select(Experience).where(Experience.id==experience_id))

    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, experience=experience,
                        user=current_user) 
      
      # here the back-referencing works - comment.experience is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 

    # using redirect sends a GET request to experience.show
    return redirect(url_for('experience.show', id=experience.id))


@eventbp.route('/<int:experience_id>/process_ticket_selection', methods=['GET', 'POST'])
@login_required
def process_ticket_selection(experience_id):
    # Create an instance of TicketSelectorForm
    ticket_selector_form = TicketSelectorForm()

    # Retrieve the selected ticket quantity from the form
    ticket_qty = int(request.form['ticket_selector'])
    print("Selected ticket quantity:", ticket_qty)

    # Retrieve the experience ID from the form
    experience_id = ticket_selector_form.experience_id.data

    # Set the choices for the ticket_selector field
    ticket_selector_form.ticket_selector.choices = [
        (i, str(i)) for i in range(ticket_qty + 1)]

    print("Inside form validated field")

    # Get the experience based on the experience ID
    experience = Experience.query.get(experience_id)

    # Check if the selected number of tickets is valid
    if ticket_qty > experience.ticket_qty:
        flash('Invalid ticket quantity selected.')
        # Redirect to an appropriate route
        return redirect(url_for('your_experiences_route'))

    # Update ticket quantity in the experience
    experience.ticket_qty -= ticket_qty

    # If tickets are sold out, update the status
    if experience.ticket_qty == 0:
        experience.status = 'Sold Out'

    # Create a new booking
    booking = Booking(
        purchased_ticket_qty=ticket_qty,
        user_id=current_user.id,
        experience_id=experience_id,
        purchase_date=datetime.utcnow()
    )

    # Add and commit the changes to the database
    db.session.add(booking)
    db.session.commit()

    return render_template('experiences/show.html', experience=experience, form=ticket_selector_form)
    # else:
      #     # Form did not validate, handle this case
      #     flash('Form did not validate.')
      #     # Redirect to an appropriate route
      #     return redirect(url_for('experiences.show', id=experience_id))

