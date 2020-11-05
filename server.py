"""Server for Sleep app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

import os
import requests

from jinja2 import StrictUndefined

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined

# FIXME NOTE:This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = True

# FIXME NOTE: Custom error message in case API doesn't exist ; user must get their own
# try:
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
API_KEY = os.environ["YOUTUBE_KEY"]
# except:
# raise
# print("No key avaliable")

# Routes start here:
@app.route("/")
def create_homepage():
    """Return homepage"""

    return render_template("homepage.html")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

# NOTE: CHECKING users emails routes added here. Just for CHECK
@app.route("/users")
def display_users_email():
    """Show all users email addresses and link to user's profile"""

    users_emails = crud.get_user_email()

    return render_template("user_details.html", users_emails=users_emails)


@app.route("/users/<user_id>")
def display_user_profile(user_id):
    """Show user's profile containing user's email"""

    user_profile = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user_profile=user_profile)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    check_email = crud.get_user_by_email(email)

    if check_email == None:
        crud.create_user(email, password)
        flash("New account created successfully! Please log in")
    else:
        flash("Email is associated with an account. Try again")

    return redirect("/")
