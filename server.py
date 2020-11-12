"""Server for Sleep app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud
import YouTube

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


# =====================================================================
# NOTE: Playlist and Video Routes Start Here:


@app.route("/video-playlist/<user_id>")
def playlist_video_page(user_id):
    """Return playlist and video options """

    return render_template("playlist-video.html", user_id=user_id)


@app.route("/video-categories/<user_id>")
def video_category_list(user_id):
    """Return list of video category selections"""

    return render_template("video-categories.html", user_id=user_id)


# NOTE: GET request after user inputs what video and video duration they want
@app.route("/video-selection/<user_id>")
def display_video_selection(user_id):
    """Query selected video filter and display to frontend"""

    video_category = request.args.get("video-category")
    video_duration = request.args.get("duration")

    display_videos = crud.display_selected_videos(video_category, video_duration)

    # TODO FIXME: This function, the CATEGORY table, may cause future problems or might not be needed? For a table category, is it necessary to keep track of in database?

    session["videos"] = (
        display_videos,
        video_category,
        video_duration,
    )  # NOTE: Store video selected list in a session with the video duration added at the end)
    print(session["videos"])

    return render_template(
        "video-displays.html", user_id=user_id, display_videos=display_videos
    )


@app.route("/register-videos/<user_id>", methods=["POST"])
def register_videos(user_id):
    """Store video and playlist in video database"""

    # TODO: Not sure of this session will cause future bugs, for example, session won't clear until user clears cache...thus, possiblity of bug when adding videos to database?
    # NOTE: Get video id list from what user selected from HTML form

    # NOTE: Playlist Creation functions begin here
    playlist_name = request.form.get("playlist-name")
    print(playlist_name)

    playlist_obj = crud.create_playlist(playlist_name, user_id)
    playlist_id = playlist_obj.playlist_id  # PRINTS THE PLAYLIST ID

    # NOTE: Video Creation function begin here:
    video_list = request.form.getlist("video-list")
    print(video_list)

    print(session["videos"])

    # NOTE: assign list of video ids only from tuple list
    n = 1  # N. . .
    video_url_id = [video[n] for video in session["videos"][0]]
    print(video_url_id)

    # Prints the title of videos only!! From the tuple list
    n = 0  # N. . .
    video_title = [video[n] for video in session["videos"][0]]

    # NOTE:prints video duration which is either short, medium, long
    print(session["videos"][2])
    video_duration = session["videos"][2]

    # NOTE: prints video category name which consist of many categories like rain, ocean, fan, etc
    print(session["videos"][1])
    video_category_name = session["videos"][1]

    # Combine the two lists above into a dictionary using dictionary comprehension method
    dict_video = {video_url_id[i]: video_title[i] for i in range(len(video_url_id))}
    print(dict_video)

    for video_ids in video_list:
        # NOTE: Will this slow down runtime???
        # NOTE: If the video ids from what user selected is equal to the video url id stored in session, then add the videos to CRUD
        if video_ids in video_url_id:
            video_title = dict_video[video_ids]
            print(video_title)
            crud.create_video(video_title, video_duration, video_ids, playlist_id)
            # crud.create_category(video_category_name)

    return render_template(
        "playlist.html",
        user_id=user_id,
        video_list=video_list,
        playlist_obj=playlist_obj,
    )


# NOTE: This next part is after user adds videos to their first, second, etc playlist. Now they can go view what current videos they have
@app.route("/current-playlist/<user_id>")
def view_playlist(user_id):
    """Return videos stored in playlist"""

    user_obj = crud.check_user_to_playlist_id(user_id)
    print(user_obj)

    return render_template("current_playlists.html", user_obj=user_obj)


@app.route("/display-playlist-videos/<playlist_id>")
def display_videos_in_playlist(playlist_id):
    """Return videos in selected playlist"""

    playlist_video_obj = crud.get_videos_from_playlist_id(playlist_id)
    print(playlist_video_obj)

    return render_template(
        "display_playlist_videos.html", playlist_video_obj=playlist_video_obj
    )


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
