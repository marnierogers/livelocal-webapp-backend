from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, EmailField, DecimalField
from wtforms.validators import InputRequired, Email, EqualTo, Regexp, NumberRange, Length
from flask_wtf.file import FileRequired, FileField, FileAllowed
import re
from wtforms.validators import ValidationError

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}


def validate_contact_number(form, field):
    print("Form validated")
    if not field.data.isdigit():
        raise ValidationError('Contact number must contain only numbers.')


# #Create new destination
# class DestinationForm(FlaskForm):
#   name = StringField('Country', validators=[InputRequired()])
#   description = TextAreaField('Description',
#                               validators=[InputRequired()])
#   image = FileField('Destination Image', validators=[
#       FileRequired(message='Image cannot be empty'),
#       FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
#   currency = StringField('Currency', validators=[InputRequired()])
#   submit = SubmitField("Create")


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
        Regexp(r"^[a-zA-Z-' ]*$",
               message="Name can only contain letters, hyphens, and apostrophes")
    ])
    email_id = EmailField("Email Address", validators=[InputRequired(),
                           Email("Please enter a valid email")])
    
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
    postcode = StringField("Postcode", validators=[
        InputRequired(),
        Regexp('^\d{4}$', message="Postcode must be a 4-digit number")
    ])

    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match"),
        Regexp('^(?=.*[A-Za-z])(?=.*[@#$%^&!]).{5,}$',
               message='Password must contain at least 1 letter, 1 special character, and be 5 characters long.')
    ])

    confirm = PasswordField("Confirm Password", validators=[InputRequired()])

    submit = SubmitField("Register", render_kw={
                         'class': 'ourClasses', 'style': 'width:100%; background-color: #849BFF; border-color: #849BFF;'})

# #User comment
# class CommentForm(FlaskForm):
#   text = TextAreaField('Comment', [InputRequired()])
#   submit = SubmitField('Create')
