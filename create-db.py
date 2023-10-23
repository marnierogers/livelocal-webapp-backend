# from website import db, create_app
# app = create_app()
# ctx = app.app_context()
# ctx.push()
# db.create_all()
# quit()


from website import db, create_app
from website.models import User  # Import the User model

app = create_app()
ctx = app.app_context()
ctx.push()

# Create the database tables
db.create_all()

# Create a new user
new_user = User(
    name="test",
    email_id="test@gmail.com",
    password_hash="Password1!",
    contact_number="your_contact_number",
    address_line1="your_address_line1",
    suburb="your_suburb",
    postcode="0000",
    avatar="your_avatar_url"
)

# Add the user to the database session

# Commit the changes to the database
db.session.commit()

# Don't forget to pop the app context to avoid potential resource leaks
ctx.pop()
