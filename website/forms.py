from flask_wtf import FlaskForm
from wtforms.fields import HiddenField, TextAreaField, SubmitField, StringField, PasswordField, EmailField, DecimalField, SelectField, DateField, MultipleFileField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp, NumberRange, Length
from wtforms import DateField, validators

from flask_wtf.file import FileRequired, FileField, FileAllowed
import re
from wtforms.validators import ValidationError
from datetime import date, datetime


ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}


def validate_contact_number(form, field):
    print("Form validated")
    if not field.data.isdigit():
        raise ValidationError('Contact number must contain only numbers.')


def validate_future_date(form, field):
    if field.data <= date.today():
        raise validators.ValidationError('Event date must be in the future.')

#User login
class LoginForm(FlaskForm):
    email_id = StringField("Email", validators=[
                            InputRequired('Enter email')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter password')])
    submit = SubmitField("Login", render_kw={
                         'class': 'ourClasses', 'style': 'width:100%; background-color: #849BFF; border-color: #849BFF;'})

#User register
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        InputRequired(),
        Regexp(r"^[a-zA-Z-' ]*$",message="Name can only contain letters, hyphens, and apostrophes")])
    email_id = EmailField("Email Address", validators=[InputRequired(),Email("Please enter a valid email")])
    
    # Added contact number field
    contact_number = StringField("Contact Number", validators=[
        InputRequired(),
        Regexp(
            '^04[0-9]{8}$', message="Contact number must start with '04' and be followed by 8 digits between 0-9")
    ])

    address_line1 = StringField("1st Line of Address", validators=[
        InputRequired(),
        Length(min=5, message="Address should be at least 5 characters long")
    ])
    suburb = StringField("Suburb", validators=[InputRequired()])
    postcode = StringField("Postcode", validators=[InputRequired(),Regexp('^\d{4}$', message="Postcode must be a 4-digit number")])

    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match"),
        Regexp('^(?=.*[A-Za-z])(?=.*[@#$%^&!]).{5,}$',
               message='Password must contain at least 1 letter, 1 special character, and be 5 characters long.')
    ])

    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

    submit = SubmitField("Register", render_kw={
                         'class': 'ourClasses', 'style': 'width:100%; background-color: #849BFF; border-color: #849BFF;'})


#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

class ExperienceForm(FlaskForm):
    type = SelectField('Type of Event', choices=[
        ('', 'Select event type'),
        ('ArtCulture', 'Art & Culture'),
        ('Tours', 'Tours'),
        ('FoodDrink', 'Food & Drink'),
        ('Unique', 'Unique')
    ], validators=[InputRequired()])
    name = StringField('Experience Name', validators=[InputRequired(message="Please enter the experience name."), Length(
        min=5, max=80, message="Name must be 5 or more characters and cannot exceed 80 characters.")])
    description = TextAreaField('Description', validators=[
        InputRequired(message="Please enter the experience description."),
        Length(min=5, max=1500, message="Description must be 5 or more characters and cannot exceed 1500 characters.")
    ])    
    address_line1 = StringField('Address', validators=[InputRequired()])
    suburb = StringField('Suburb', validators=[InputRequired()])
    postcode = StringField("Postcode", validators=[InputRequired(),Regexp('^\d{4}$', message="Postcode must be a 4-digit number")])
    start_date = DateField('Event Date', format='%Y-%m-%d',validators=[InputRequired()])
    
    start_time = TimeField('Start Date and Time', validators=[validators.InputRequired()])
    end_time = TimeField('End Date and Time', validators=[validators.InputRequired()])
    
    # start_time = StringField("Start Time (hh:mm)", validators=[InputRequired(), Regexp(
    #     '^([01]\d|2[0-3]):([0-5]\d)$', message="Start time must be in hh:mm 24-hr format")])
    # end_time = StringField("End Time (hh:mm)", validators=[InputRequired(), Regexp(
    #     '^([01]\d|2[0-3]):([0-5]\d)$', message="End time must be in hh:mm 24-hr format")])
    ticket_qty = SelectField('Number of Tickets', choices=[(str(i), str(i)) for i in range(1, 21)], validators=[InputRequired()])    
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(
        min=0.01, max=500,  message="Price must be between 0.01 and 500.")])
    
    image_1 = FileField('Image 1 (must upload a minimum 3 images)', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    
    image_2 = FileField('Image 2', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    
    image_3 = FileField('Image 3', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])

    submit = SubmitField('Create Now')

    def validate_end_time(self, field):
        start_time = self.start_time.data
        end_time = field.data
        if start_time and end_time and end_time <= start_time:
            raise ValidationError("End time cannot be earlier than or equal to the start time")


class TicketSelectorForm(FlaskForm):
    ticket_selector = SelectField('Tickets:', coerce=int, validators=[InputRequired()])
    experience_id = HiddenField()
    submit = SubmitField('Book Now')

    # def set_ticket_choices(self, max_ticket_qty):
    #     self.ticket_selector.choices = [(i, str(i))
    #                                     for i in range(max_ticket_qty + 1)]
