from datetime import datetime
from .models import Experience
from . import db
from PIL import Image


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
