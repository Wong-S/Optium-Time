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

# ================================================================================
# Routes start here:
@app.route("/")
def create_homepage():
    """Return homepage"""

    return render_template("homepage.html")


# ================================================================================
# NOTE: CHECKING users emails routes added here. Just for CHECK FIXME: REMOVE LATER
@app.route("/users")
def display_users_email():
    """Show all users email addresses and link to user's profile"""

    users_emails = crud.get_user()

    return render_template("user_details.html", users_emails=users_emails)


@app.route("/users/<user_id>")
def display_user_profile(user_id):
    """Show user's profile containing user's email"""

    user_profile = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user_profile=user_profile)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user account"""

    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    check_email = crud.get_user_by_email(email)

    if check_email == None:
        crud.create_user(first_name, last_name, email, password)
        flash(
            "New account created successfully! Please log in"
        )  # FIXME: Change Flash messages!!!

    else:
        flash("Email is associated with an account. Try again!")

    return redirect("/")


@app.route("/login")
def check_login_credentials():
    """Return journal webpage or redirect to homepage"""

    email = request.args.get("login_email")
    password = request.args.get("login_password")

    match_passwords = crud.check_password(email, password)

    user_details = crud.get_user_by_email(
        email
    )  # NOTE: Return the specified OBJECT relating to that exact email. From there, can call instance attributes

    if match_passwords == True:
        flash("Logged in!")
        return render_template("user_page.html", user=user_details)
    else:
        flash("Email or password do not match. Try again!")
        return redirect("/")


# =====================================================================
# User Page Route: What displays here is Journals, Sleep Log, Playlists Selection, etc:


# @app.route("/user-page")
# def display_user_options():
#     """Return user's next selection"""

#     return render_template("user_page.html")


# =====================================================================
# NOTE: Journal Entry Routes Start Here:
@app.route("/journal/<user_id>")
def journal_entry(user_id):
    """Return journal page """

    return render_template(
        "journal.html", user_id=user_id
    )  # NOTE:Passing in the user's ID here!


# NOTE: CHECKING if Journal Entries actually got seeded and display correctly
@app.route("/journal-current-entries/<user_id>")
def display_journal_information(user_id):
    """Show all user's journal information"""

    user_obj = crud.check_user_to_journal_id(user_id)

    return render_template("journal_details.html", user_obj=user_obj)


@app.route("/journal-new-entries/<user_id>")
def display_new_journal(user_id):
    """Return new journal page"""

    return render_template("journal_creation.html", user_id=user_id)


# NOTE: Need to ensure ID match to make a journal entry!
@app.route("/journals/<user_id>", methods=["POST"])
def register_journal_entry(user_id):
    """Create a new journal entry per user"""

    entry_name = request.form.get("entry-name")
    entry_details = request.form.get("entry-details")
    user_id = int(
        user_id
    )  # NOTE FIXME: CODE REVIEW ?? Does a Foreign Key really need to be specified here? And converted from user_id string to int?

    # if user_id matches True:
    crud.create_journal_entry(user_id, entry_name, entry_details)
    flash("New entry made!!")

    return render_template("journal.html", user_id=user_id)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
