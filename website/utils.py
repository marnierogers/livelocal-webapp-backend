from datetime import datetime
from .models import Experience
from . import db


def update_experience_statuses():
    current_time = datetime.now()
    experiences = Experience.query.all()

    for experience in experiences:
        if experience.start_time < current_time and experience.status != "Cancelled":
            experience.status = "Inactive"
            db.session.commit()
