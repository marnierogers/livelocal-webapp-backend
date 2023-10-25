from datetime import datetime
from .models import Experience
from . import db
from PIL import Image
import os
from werkzeug.utils import secure_filename


def update_experience_statuses():
    current_time = datetime.now()
    experiences = Experience.query.all()

    for experience in experiences:
        if experience.start_time < current_time and experience.status != "Cancelled":
            experience.status = "Inactive"
            db.session.commit()


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
