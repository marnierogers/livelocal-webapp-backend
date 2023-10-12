from flask import Blueprint, render_template, redirect, url_for, flash
from flask import Markup
from website.forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

global count
count = 1

#create a blueprint
authbp = Blueprint('auth', __name__ )

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    global count
    register = RegisterForm()
    
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):

            #get username, password and email from the form
            name = register.name.data
            pwd = register.password.data
            email_id = register.email_id.data
            contact_number = register.contact_number.data
            address_line1 = register.address_line1.data
            suburb = register.suburb.data
            postcode = register.postcode.data
            avatar = f"../static/img/avatars/avatar{count}.png"

            count = count + 1

            #check if a user exists
            emailid = db.session.scalar(db.select(User).where(User.email_id==email_id))
            if emailid:  # this returns true when user is not None
                flash('Email already exists, please try another', 'error')
                return redirect(url_for('auth.register'))
            
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)

            #create a new User model object
            new_user = User(name=name, password_hash=pwd_hash, email_id=email_id,
                            contact_number=contact_number, address_line1=address_line1, suburb=suburb, postcode=postcode, avatar=avatar)
            db.session.add(new_user)
            db.session.commit()

            #commit to the database and redirect to HTML page
            return redirect(url_for('auth.login'))
    
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register Now', 
                               top_copy='Your next memorable adventure starts here. Sign up now to join, craft and host one-of-a-kind experiences with memories that will last a lifetime.', 
                               bottom_copy=Markup("Already have an account? Click <a href='/login'>here</a> to login now."))


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):

        #get the username and password from the database
        email_id = login_form.email_id.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email_id==email_id))

        #if there is no user with that name
        if user is None:
            error = 'Please enter a valid email and password'

        #check the password - notice password hash function
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error = 'Incorrect password'
        if error is None:
            
            #all good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login', 
                           top_copy="You're 1-click away from your next big adventure! Enter your details to login to get started.", 
                           bottom_copy=Markup("Don't have an account? Click <a href='/register'>here</a> to register now."))


@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
