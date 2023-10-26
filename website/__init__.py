from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv  # Import dotenv
import datetime

load_dotenv()

db = SQLAlchemy()
app = Flask(__name__)


def create_app():

    #we use this utility module to display forms quickly
    bootstrap = Bootstrap5(app)

    #this is a much safer way to store passwords
    bcrypt = Bcrypt(app)

    #a secret key for the session object
    #(it would be better to use an environment variable here)
    app.secret_key = os.getenv('SECRET_KEY')

    #Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = 'static/upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.bp)
    from . import experiences
    app.register_blueprint(experiences.eventbp)

    from .auth import authbp
    app.register_blueprint(authbp)

    return app

# inbuilt function which takes error as parameter
@app.errorhandler(404)
def not_found(e):
  return render_template("errors/error.html", status_code=404)

@app.context_processor
def get_context():
   year = datetime.datetime.today().year
   return dict(year=year)
