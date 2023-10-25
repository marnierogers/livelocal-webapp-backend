from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import Experience, Comment, Booking
from .forms import ExperienceForm, CommentForm, TicketSelectorForm, UpdateExperienceForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from datetime import datetime
from .models import User
from .utils import update_experience_statuses
from PIL import Image


eventbp = Blueprint('experience', __name__, url_prefix='/experiences')


@eventbp.route('/<id>')
def show(id):
    experience = db.session.scalar(db.select(Experience).where(Experience.id==id))

    print(experience)
    update_experience_statuses()
    
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
  update_experience_statuses()
  
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

    # # Call the function that checks and returns image
    # db_file_path = check_upload_file(form)
    # db_file_path_2 = check_upload_file_2(form)
    # db_file_path_3 = check_upload_file_3(form)

    # Check image dimensions
    if image_1:
        if not is_valid_image_dimension(image_1, width=800, height=1000):
            form.image_1.errors.append("Image 1 must be 800x1000 pixels")
            return render_template('experiences/create.html', form=form)

        db_file_path = check_upload_file(form)

    if image_2:
        if not is_valid_image_dimension(image_2, width=800, height=1000):
            form.image_2.errors.append("Image 1 must be 800x1000 pixels")
            return render_template('experiences/create.html', form=form)

        db_file_path_2 = check_upload_file(form)

    if image_3:
        if not is_valid_image_dimension(image_3, width=800, height=1000):
            form.image_3.errors.append("Image 1 must be 800x1000 pixels")
            return render_template('experiences/create.html', form=form)

        db_file_path_3 = check_upload_file(form)
    
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

    update_experience_statuses()

    return render_template('experiences/update.html', experiences=experiences)


@eventbp.route('/update_event/<int:experience_id>', methods=['GET', 'POST'])
@login_required
def update_page(experience_id):
    print('Method type: ', request.method)

    # Get the experience object by id and check if it belongs to the current user
    experience = Experience.query.get(experience_id)

    # Create an instance of the UpdateExperienceForm without obj
    form = UpdateExperienceForm()

    # Add a print statement to check the experience
    print('Experience:', experience)

    if request.method == 'POST':
        print("Inside POST request")
        if form.validate():
            print("Form is valid")

            # Update the experience object with the new form data
            form.populate_obj(experience)

            # Adjust start and end time
            start_date = form.start_date.data
            start_time = form.start_time.data
            end_time = form.end_time.data
            experience.start_time = datetime.combine(start_date, start_time)
            experience.end_time = datetime.combine(start_date, end_time)

            # Call the function that checks and returns image
            # Check image dimensions
            image_1 = form.image_1.data
            image_2 = form.image_2.data
            image_3 = form.image_3.data

            if image_1:
                if not is_valid_image_dimension(image_1, width=800, height=1000):
                    form.image_1.errors.append("Image 1 must be 800x1000 pixels")
                    return render_template('experiences/create.html', form=form)

                db_file_path = check_upload_file(form)

            if image_2:
                if not is_valid_image_dimension(image_2, width=800, height=1000):
                    form.image_2.errors.append("Image 1 must be 800x1000 pixels")
                    return render_template('experiences/create.html', form=form)

                db_file_path_2 = check_upload_file(form)

            if image_3:
                if not is_valid_image_dimension(image_3, width=800, height=1000):
                    form.image_3.errors.append("Image 1 must be 800x1000 pixels")
                    return render_template('experiences/create.html', form=form)

                db_file_path_3 = check_upload_file(form)

            # Update the image paths
            experience.image_1 = db_file_path
            experience.image_2 = db_file_path_2
            experience.image_3 = db_file_path_3

            db.session.commit()
            flash('Experience successfully updated.','Experience successfully updated.')
            return redirect(url_for('experience.update', experience_id=experience.id))

        else:
            print("Form is invalid")
            print("Form errors:", form.errors)


    # Manually set the form fields using data from the experience object
    form.type.data = experience.type
    form.name.data = experience.name
    form.description.data = experience.description
    form.address_line1.data = experience.address_line1
    form.suburb.data = experience.suburb
    form.postcode.data = experience.postcode
    form.start_date.data = experience.start_date
    form.start_time.data = experience.start_time
    form.end_time.data = experience.end_time
    form.ticket_qty.data = experience.ticket_qty
    form.price.data = experience.price
    form.image_1.data = experience.image_1
    form.image_2.data = experience.image_2
    form.image_3.data = experience.image_3

    return render_template('experiences/update_event.html', form=form, experience=experience)




@eventbp.route('/cancel_event/<int:experience_id>', methods=['POST'])
def cancel_event(experience_id):

    # Find the experience by ID
    experience = Experience.query.get(experience_id)

    update_experience_statuses()

    if experience:
        # Update the status to "Cancelled"
        experience.status = "Cancelled"
        db.session.commit()

    return redirect(url_for('experience.update'))



def is_valid_image_dimension(file, width, height):
    try:
        image = Image.open(file)
        return image.width == width and image.height == height
    except Exception:
        return False



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
    update_experience_statuses()

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

    update_experience_statuses()

    # Get the experience based on the experience ID
    experience = Experience.query.get(experience_id)

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

   # Determine the message for singular or plural tickets
    message = "tickets" if ticket_qty > 1 else "ticket"

    # Set a flash message with the experience ID
    flash(
        f"Success! You've purchased {ticket_qty} {message}. Your booking ID is {booking.booking_id}.", 'success')

    return render_template('experiences/show.html', experience=experience, form=ticket_selector_form)
