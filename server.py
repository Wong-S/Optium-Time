"""Server for Sleep app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
import datetime_functions
import YouTube

import os
import requests

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

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

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)
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
    timezone = request.form.get("timezone")

    # NOTE:Store user's timezone selection into session; print to check

    check_email = crud.get_user_by_email(email)

    if check_email == None:
        crud.create_user(first_name, last_name, email, password, timezone)
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
        # flash("Logged in!")

        # NOTE: Storing user primary id in a session
        session["user"] = user_details.user_id
        print(session["user"])
        session["user_name"] = user_details.first_name

        # NOTE: Storing user's timezone in a session
        session["timezone"] = user_details.timezone
        print(session["timezone"])

        return redirect("/user-page")
    else:
        flash("Email or password do not match. Try again!")
        return redirect("/")


# =====================================================================
# User Page Route: What displays here is Journals, Sleep Log, Playlists Selection, etc:


@app.route("/user-page", methods=["GET", "POST"])
def display_user_options():
    """Return user's next selection"""

    user_id = session["user"]

    user_obj = crud.get_user_by_id(user_id)

    # print("GET THE HIDDEN INPUT WITHOUT A FORM SUBMISSION")
    # x = request.form.get("send-text")
    # print(x)

    print("IF YOU MADE IT HERE!!!!")

    # TODO !!!!! FIX BUG WHEN YOU RESTART A NEW SERVER WITHOUT AN ALARM SET! Basically once the session is cleared it messes up....
    # FIXME: NOT SURE IF THE BELOW WORKS.....
    ###########################################################
    # WRITE A CONDITIONAL HERE TO BYPASS THIS PROBLEM???
    user_timezone = session["timezone"]
    print("User's TIMEZONE for the month is:", user_timezone)

    chosen_month_by_user_str = datetime_functions.current_date_timezone_from_utc_with_month_format(
        user_timezone
    )

    print("THE TYPE OF THE CURRENT MONTH DATE IS:")
    # print(type(chosen_month_by_user_obj))  # A datetime.date obj

    # chosen_month_by_user_str = str(chosen_month_by_user_obj)
    print(type(chosen_month_by_user_str))

    print("THE CHOSEN MONTH BY USER WAS:", chosen_month_by_user_str)

    sleep_log_user_obj = crud.get_sleep_data_user_id(
        user_id
    )  # <User user_id = 1 first_name = Shelby>

    print("ALL THE USER'S  DATA IS:", sleep_log_user_obj)

    # Now I need to call the joined sleep_log table
    all_date_obj_lst = []
    for data in sleep_log_user_obj.sleep_logs:
        print(data.current_date)  # 2020-11-25
        print(type(data.current_date))  # <class 'datetime.date'>
        # print(data.current_date[0]) #ERROR! NOT SCRIPTABLE
        all_date_obj_lst.append(data.current_date)

    print(
        "LIST OF ALL DATE OBJECTS IS:", all_date_obj_lst
    )  # [datetime.date(2020, 11, 1), datetime.date(2020, 11, 2), datetime.date(2020, 11, 3), datetime.date(2020, 11, 4), datetime.date(2020, 11, 5), datetime.date(2020, 11, 6), datetime.date(2020, 11, 7), datetime.date(2020, 11, 8), datetime.date(2020, 11, 9), datetime.date(2020, 11, 10), datetime.date(2020, 11, 11), datetime.date(2020, 11, 12), datetime.date(2020, 11, 13), datetime.date(2020, 11, 14), datetime.date(2020, 11, 15), datetime.date(2020, 11, 16), datetime.date(2020, 11, 17), datetime.date(2020, 11, 18), datetime.date(2020, 11, 19), datetime.date(2020, 11, 20), datetime.date(2020, 11, 21), datetime.date(2020, 11, 22), datetime.date(2020, 11, 23), datetime.date(2020, 11, 24), datetime.date(2020, 11, 25), datetime.date(2020, 11, 26), datetime.date(2020, 11, 27)]
    ##############
    # I Can do The following steps:
    # 1. Store the datetime in a list
    # 2. Convert that list to a string format with only the 2020-11 present
    ##############
    all_datetime_str_lst = datetime_functions.create_date_str(all_date_obj_lst)
    print(
        "ALL DATES AS A STRING IS:", all_datetime_str_lst
    )  # ['2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11']

    # NOW, need to take the all_date_obj_lst and convert to the converted string dates "2020-11-1"
    converted_dates_obj_to_str = datetime_functions.convert_date_obj_to_str_format(
        all_date_obj_lst
    )

    print(
        "IF YOU MAKE IT HERE THE ALL STRINGS DATES ARE:", converted_dates_obj_to_str
    )  # ['2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27']

    # Now combine the converted string dates and the HTML selected month dates into a dict:
    all_month_dict = {
        converted_dates_obj_to_str[i]: all_datetime_str_lst[i]
        for i in range(len(converted_dates_obj_to_str))
    }

    print(
        "THE DICTIONARY FOR MONTHS IS:", all_month_dict
    )  # {'2020-11-01': '2020-11', '2020-11-02': '2020-11', '2020-11-03': '2020-11', '2020-11-04': '2020-11', '2020-11-05': '2020-11', '2020-11-06': '2020-11', '2020-11-07': '2020-11', '2020-11-08': '2020-11', '2020-11-09': '2020-11', '2020-11-10': '2020-11', '2020-11-11': '2020-11', '2020-11-12': '2020-11', '2020-11-13': '2020-11', '2020-11-14': '2020-11', '2020-11-15': '2020-11', '2020-11-16': '2020-11', '2020-11-17': '2020-11', '2020-11-18': '2020-11', '2020-11-19': '2020-11', '2020-11-20': '2020-11', '2020-11-21': '2020-11', '2020-11-22': '2020-11', '2020-11-23': '2020-11', '2020-11-24': '2020-11', '2020-11-25': '2020-11', '2020-11-26': '2020-11', '2020-11-27': '2020-11'}

    # Now return only the selected months and string dates associated with tht HTML choosen date values from the dict and RETURN a new list with those months
    selected_month_filter_str_lst = []

    for k, v in all_month_dict.items():
        if v == chosen_month_by_user_str:
            # print(v)
            # print(k)
            selected_month_filter_str_lst.append(k)

    print(
        "Filtered OUT MONTHS FROM CHOSEN HTML DATE ARE:", selected_month_filter_str_lst
    )  # ['2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27']

    # TODO FINISH HERE 11/28 !!!!!
    # Now take that list of strings and convert back to datetime.date obj. Then do a crud filter for those objects and get the wake,bed time info. Look above on line 476 for how to do it with the last grouped dates!

    month_date_obj_lst = datetime_functions.create_filtered_date_obj_from_str_lst(
        selected_month_filter_str_lst
    )

    print(
        "CONVERTED MONTHS FROM STR TO OBJ LST:", month_date_obj_lst
    )  # [datetime.datetime(2020, 11, 1, 0, 0), datetime.datetime(2020, 11, 2, 0, 0), datetime.datetime(2020, 11, 3, 0, 0), datetime.datetime(2020, 11, 4, 0, 0), datetime.datetime(2020, 11, 5, 0, 0), datetime.datetime(2020, 11, 6, 0, 0), datetime.datetime(2020, 11, 7, 0, 0), datetime.datetime(2020, 11, 8, 0, 0), datetime.datetime(2020, 11, 9, 0, 0), datetime.datetime(2020, 11, 10, 0, 0), datetime.datetime(2020, 11, 11, 0, 0), datetime.datetime(2020, 11, 12, 0, 0), datetime.datetime(2020, 11, 13, 0, 0), datetime.datetime(2020, 11, 14, 0, 0), datetime.datetime(2020, 11, 15, 0, 0), datetime.datetime(2020, 11, 16, 0, 0), datetime.datetime(2020, 11, 17, 0, 0), datetime.datetime(2020, 11, 18, 0, 0), datetime.datetime(2020, 11, 19, 0, 0), datetime.datetime(2020, 11, 20, 0, 0), datetime.datetime(2020, 11, 21, 0, 0), datetime.datetime(2020, 11, 22, 0, 0), datetime.datetime(2020, 11, 23, 0, 0), datetime.datetime(2020, 11, 24, 0, 0), datetime.datetime(2020, 11, 25, 0, 0), datetime.datetime(2020, 11, 26, 0, 0), datetime.datetime(2020, 11, 27, 0, 0)]

    # Now take the list of datetime.date objects and do a query filter to get the wake and bed times
    user_sleep_log_obj_for_date_lst = crud.get_sleep_time_by_filtered_month_lst(
        user_id, month_date_obj_lst
    )

    print(
        "USER OBJ WITH THOSE FILTERED DATE MONTHS:", user_sleep_log_obj_for_date_lst
    )  # [<SleepLog sleep_log_id = 1 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-01>, <SleepLog sleep_log_id = 2 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-02>, <SleepLog sleep_log_id = 3 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-03>, <SleepLog sleep_log_id = 4 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-04>, <SleepLog sleep_log_id = 5 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-05>, <SleepLog sleep_log_id = 6 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-06>, <SleepLog sleep_log_id = 7 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-07>, <SleepLog sleep_log_id = 8 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-08>, <SleepLog sleep_log_id = 9 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-09>, <SleepLog sleep_log_id = 10 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-10>, <SleepLog sleep_log_id = 11 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-11>, <SleepLog sleep_log_id = 12 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-12>, <SleepLog sleep_log_id = 13 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-13>, <SleepLog sleep_log_id = 14 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-14>, <SleepLog sleep_log_id = 15 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-15>, <SleepLog sleep_log_id = 16 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-16>, <SleepLog sleep_log_id = 17 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-17>, <SleepLog sleep_log_id = 18 wake_time = 10:30:00 bed_time = 23:11:00 current_date = 2020-11-18>, <SleepLog sleep_log_id = 19 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-19>, <SleepLog sleep_log_id = 20 wake_time = 10:30:00 bed_time = 23:11:00 current_date = 2020-11-20>, <SleepLog sleep_log_id = 21 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-21>, <SleepLog sleep_log_id = 22 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-22>, <SleepLog sleep_log_id = 23 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-23>, <SleepLog sleep_log_id = 24 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-24>, <SleepLog sleep_log_id = 25 wake_time = 05:55:00 bed_time = 23:42:52 current_date = 2020-11-25>, <SleepLog sleep_log_id = 26 wake_time = 08:33:00 bed_time = 12:20:21 current_date = 2020-11-26>, <SleepLog sleep_log_id = 27 wake_time = 06:30:00 bed_time = 17:55:33 current_date = 2020-11-27>]

    timezone = session["timezone"]
    print("USER TIMEZONE CURRENTLY IS:", timezone)

    total_time_hours_lst = []
    for i in user_sleep_log_obj_for_date_lst:
        total_subtracted_hours = datetime_functions.time_difference(
            timezone, i.wake_time, i.bed_time
        )
        total_time_hours_lst.append(total_subtracted_hours)

    print(
        "THE TOTAL TIME HOURS IS", total_time_hours_lst
    )  # [8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 10.19, 11.19, 8.19, 11.19, 10.19, 10.19, 10.19, 10.19, 6.12, 20.12, 12.34]

    # Now convert the datetime obj list to formatted strings to be displayed to the front end!
    #   1. Will pick two displays: Currently We have: Nov 1 (looks cluttered)
    #   2. 11/1/20
    #   3/ 11/1

    # Type string format #1:
    month_date_converted_to_str = datetime_functions.create_date_str_with_different_format(
        month_date_obj_lst
    )

    print(
        "THE FIRST TYPE:", month_date_converted_to_str
    )  # ['11/01', '11/02', '11/03', '11/04', '11/05', '11/06', '11/07', '11/08', '11/09', '11/10', '11/11', '11/12', '11/13', '11/14', '11/15', '11/16', '11/17', '11/18', '11/19', '11/20', '11/21', '11/22', '11/23', '11/24', '11/25', '11/26', '11/27', '11/28']

    # NOW STORE TIME HOURS AND MONTHS STRINGS INTO A SESSION AND PUT INTO A JSON ROUTE
    session["month_total_hours"] = total_time_hours_lst
    session["month_dates"] = month_date_converted_to_str

    print("HEY THE USER ID IS:", user_id)  # Is user_id = 1

    if "set-alarm-wake-time" in session:
        alarm_wake_time = session["set-alarm-wake-time"]
        print(type(alarm_wake_time))
        print("THE CURRENT ALARM WAKE TIME IS:", alarm_wake_time)  # STRING TYPE!!

        new_time_str = datetime_functions.format_time_str(alarm_wake_time)
        print("THE NEWLY CONVERTED ALARM WAKE TIME IS:", new_time_str)
        # alarm_set_str = "Alarm:"

        return render_template(
            "user_page.html",
            user_obj=user_obj,
            new_time_str=f"Alarm Set: {new_time_str}",
            user_id=user_id,
        )
    else:
        print("THERE IS NOTHING IN THE ALARM CLOCK SESSION")
        new_time_str = "No Alarm Set"
        return render_template(
            "user_page.html",
            user_obj=user_obj,
            new_time_str=new_time_str,
            user_id=user_id,
        )

    # if session["set-alarm-wake-time"] == None:
    #     return render_template("user_page.html", user_obj=user_obj)
    # else:
    #     alarm_wake_time = session["set-alarm-wake-time"]
    #     print(type(alarm_wake_time))
    #     print("THE CURRENT ALARM WAKE TIME IS:", alarm_wake_time)  # STRING TYPE!!

    #     new_time_str = datetime_functions.format_time_str(alarm_wake_time)
    #     print("THE NEWLY CONVERTED ALARM WAKE TIME IS:", new_time_str)

    #     return render_template(
    #         "user_page.html", user_obj=user_obj, new_time_str=new_time_str
    #     )
    ###########################################################


# # =====================================================================
# NOTE: Journal Entry Routes Start Here:
@app.route("/journal/<user_id>")
def journal_entry(user_id):
    """Return journal page """

    print("AT THE JOURNAL ROUTE THE ID IS:", user_id)

    return render_template(
        "journal_creation.html", user_id=user_id
    )  # NOTE:Passing in the user's ID here!
    # return render_template(
    #     "journal.html", user_id=user_id
    # )  # NOTE:Passing in the user's ID here!


# NOTE: CHECKING if Journal Entries actually got seeded and display correctly
@app.route("/journal-current-entries/<user_id>")
def display_journal_information(user_id):
    """Show all user's journal information"""

    user_obj = crud.check_user_to_journal_id(user_id)

    print()
    print("USER OBJECT IS FROM JOURNAL:", user_obj)
    print()

    return render_template("journal_details.html", user_obj=user_obj)


@app.route("/journal-new-entries/<user_id>")
def display_new_journal(user_id):
    """Return new journal page"""

    print(
        "ON JOURNAL CREATE THE ID IS:", user_id
    )  # NOTE: Getting this error: <user_id>

    return render_template("journal_creation.html", user_id=user_id)


# NOTE: Need to ensure ID match to make a journal entry!
@app.route("/journals/<user_id>", methods=["POST"])
def register_journal_entry(user_id):
    """Create a new journal entry per user"""

    entry_name = request.form.get("entry-name")
    entry_details = request.form.get("entry-details")

    print("WHAT IS TEH TYPE OF USER ID", user_id)
    print(type(user_id))
    # user_id = int(user_id)
    # NOTE FIXME: CODE REVIEW ?? Does a Foreign Key really need to be specified here? And converted from user_id string to int?

    timezone = session["timezone"]
    created_at = datetime_functions.current_date_timezone_from_utc(timezone)
    updated_at = datetime_functions.current_date_timezone_from_utc(timezone)

    print()
    print("The CREATED TIME AT:", created_at)
    print("The Updated time is:", updated_at)
    print()
    # if user_id matches True:

    print("THIS NEXT STEP HERE!!")

    crud.create_journal_entry(
        user_id, entry_name, entry_details, created_at, updated_at
    )
    flash("New entry made!!")

    return render_template("journal_creation.html", user_id=user_id)


# TODO: COMMENTED OUT DEUBGIGGIN 12/4
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

    video_category = request.args.getlist("categories")

    print("THE video_category LIST IS:", video_category)

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

    user_obj = crud.check_user_to_playlist_id(user_id)

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
        "current_playlists.html",
        user_id=user_id,
        video_list=video_list,
        playlist_obj=playlist_obj,
        user_obj=user_obj,
    )


# NOTE: This next part is after user adds videos to their first, second, etc playlist. Now they can go view what current videos they have
@app.route("/current-playlist/<user_id>")
def view_playlist(user_id):
    """Return videos stored in playlist"""

    user_obj = crud.check_user_to_playlist_id(user_id)
    print(user_obj)

    return render_template("current_playlists.html", user_obj=user_obj, user_id=user_id)


@app.route("/display-playlist-videos/<playlist_id>")
def display_videos_in_playlist(playlist_id):
    """Return videos in selected playlist"""

    user_id = session["user"]

    playlist_video_obj = crud.get_videos_from_playlist_id(playlist_id)
    # print(playlist_video_obj)

    return render_template(
        "display_playlist_videos.html",
        playlist_video_obj=playlist_video_obj,
        user_id=user_id,
    )


# =====================================================================
# NOTE: Start part 4: Sleep log and Alarm clock routes


@app.route("/set-alarm/<user_id>")
def display_alarm_clock(user_id):
    """Return alarm clock options"""

    return render_template("set_alarm.html", user_id=user_id)


# From set-alarm.html, got to this route below. Take in the wake-time and put to the database. THen flash message how much time between user will wake up
@app.route("/set-alarm/<user_id>", methods=["POST"])
def register_alarm(user_id):
    """Store wake up and bed time to database"""

    # NOTE: If you do an input like 4:44 PM, it'll return 16:44 ONLY. So only return Hour and Min
    wake_time = request.form.get("alarm-wake")
    print(
        wake_time
    )  # FIXME: Just a check; THIS IS A STRING!! But What is coming out is 06:30 which doesn't match the format H:M:S, so need to convert!
    # print("The HTML type WAKE time is:", type(wake_time))
    # COnvert to H:M:S by adding a ":00" string

    wake_add_sec_time = ":00"
    wake_time = wake_time + wake_add_sec_time
    # print("THE Wake_time from the alarm is NOWL", wake_time)

    session["set-alarm-wake-time"] = wake_time

    # NOTE: bed time calculation done by taking in user's current time zone from session
    user_timezone = session["timezone"]
    # print(user_timezone)  # FIXME: Just a check

    bed_time = datetime_functions.current_time_timezone_from_utc(user_timezone)
    # print(bed_time)  # FIXME: Just a check, This is a STRING formatted
    print("The HTML type BED time is:", type(bed_time))

    # NOTE: current_date calculation based on timezone because before, the date was not aware
    current_date = datetime_functions.current_date_timezone_from_utc(user_timezone)
    print(current_date)  # FIXME: This is a just a check
    session[
        "current_date"
    ] = current_date  # NOTE: This is NOT the converted datetime format, just the regular object non formated??????
    # print("The SESSION STORED is", session["current_date"])  # Just an datetime object!

    # Seed into the database what user choose for wake time
    crud.create_sleep_log(user_id, wake_time, bed_time, current_date)
    # print("THE NEXT STEP IS")

    # Find the total time user will have from bed time to wake time:
    user_total_time = datetime_functions.time_difference(
        user_timezone, wake_time, bed_time
    )

    # print("The Calculated SUBTRACT TIME is", user_total_time)
    # flash("Your alarm is set")

    # TODO CREATE A ALARM COUNTDOWN FOR THE HOMEPAGE 11/28 ---------
    # Steps I need to take is create a JSON route to store the user's alarm total alarm
    session["alarm"] = user_total_time  # 0.15 or 2.15, etc

    # print("THE STORED ALARM SESSION IS:", user_total_time)

    # TODO: TWILIO API MESSAGE CALL HAPPENS HERE #UPDATE: IT WORKS SORTA...There is a bug now where the alarm waits until countdown is over before sending a message
    # alarm_num_time = session["alarm"]
    # user_first_name = session["user_name"]
    # twilio_message = datetime_functions.countdown_message(
    #     alarm_num_time, user_first_name
    # )

    # print("YOU SHOULD HAVE RECEIVED A TEXT WITH INFORMATION ON YOUR SLEEP!!")

    #
    # return render_template("user_page.html")
    # Redirect to the homepage and see the alarm countdown clock. THen add an option to delete the alarm or not?
    return redirect("/user-page")


@app.route("/countdown.json")
def get_alarm_countdown_details():
    """Return user's alarm settings to frontend"""

    # TODO: 12/1 Bug; everytime the user refreshes the page, the alarm also refreshes and restarts.
    # TODO: every refresh gets everything again from the backend. You cannot preserve refreshes. Javascript doesn't know anything happening on the backend.
    user_alarm_details = session["alarm"]  # 7.46 (Float type)
    # TODO NOTE: Get difference between Wake and now time
    # TODO Keep in mind crossing over midnight (Remember the last issue with the hours mess up)
    #
    # print("THE ROUTE FOR THE ALARM COUNTDOWN SESSION IS:", user_alarm_details)
    # print(type(user_alarm_details))

    user_alarm_details_str = str(user_alarm_details)

    user_alarm_details_lst = user_alarm_details_str.split(".")

    alarm_hours = int(user_alarm_details_lst[0])
    alarm_minutes = int(user_alarm_details_lst[1])

    # print("THE ALARM HOURS IS:", alarm_hours)
    # print("THE ALARM MINUTES IS:", alarm_minutes)

    alarm_dict = {"hours": alarm_hours, "minutes": alarm_minutes}
    # print("ALARM DICTIONARY IS:", alarm_dict)

    return alarm_dict


# =================================================
# TODO: Once the countdown is finished, then the Twilio APP executes
# @app.route("/countdown-timer")
# def display_countdown_timer():
#     """Return countdown timer page of set alarm"""

#     print("YOU MADE IT HERE AT THIS ROUTE!!! FOR COUNTDOWN")

#     return render_template("countdown.html")

# TODO UPDATE! THIS WORKS! THE PYTHON COUNTDOWN WAS TOO SLOW
@app.route("/countdown-timer-message-twilio")
def display_countdown_timer():
    """Return countdown timer page of set alarm"""

    # print("YOU MADE IT HERE AT THIS ROUTE!!! FOR COUNTDOWN")
    alarm_num_time = session["alarm"]
    user_first_name = session["user_name"]
    twilio_message = datetime_functions.countdown_message(
        alarm_num_time, user_first_name
    )

    # TODO NEED TO CLEAR THE SESSION TO PREVENT A REFRESH EACH TIME THE PAGE LOADS AND DISPLAYS THE ALARM AGAIN AND AGAIN?
    # session["alarm"] = 0
    # print("THE MESSAGE IS:", twilio_message)

    return jsonify(twilio_message)


# =================================================
# NOTE: This parts begins the Chart.js to display user sleep in graphical model
@app.route("/sleep-log")
def display_sleep_graph_options():
    """Return sleep graphs page"""

    user_id = session["user"]
    # FIXME: Somehow, calling and passing in just user_id does NOT work! It's because we need to actually pass in the user_id from the route above, but will need to render a new template, rather than redirect

    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    # NOTE: Need to conver the date to this format in this file, not the crud file because you'll still get this output to frontend: 2020-11-13 00:00:00, which is not what I need. Just the date, not the time
    converted_current_date = []  # This list contains ALL the dates.
    for date in sleep_log_user_obj.sleep_logs:
        current_date = date.current_date
        converted_current_date.append(current_date.strftime("%b-%d-%Y"))
    ######################
    # TODO: Divide the dates by 7 days. And have that display as a hyperlink
    converted_current_date_for_grouping_obj = []

    for date in sleep_log_user_obj.sleep_logs:
        current_date = date.current_date
        # converted_current_date_for_grouping.append(current_date.strftime("%m/%d/%Y"))
        converted_current_date_for_grouping_obj.append(current_date)

    # print("CONVERTED CURRENT DATE LIST IS:", converted_current_date_for_grouping_obj)

    # Store in session for later use:
    session["dates_group_obj"] = converted_current_date

    dates_grouped_by_seven = []
    for x in range(0, len(converted_current_date_for_grouping_obj), 7):
        dates_grouped_by_seven.append(
            converted_current_date_for_grouping_obj[x : x + 7]
        )
    # FIXME: WILL DELETE AND ADD TO THE NEXT ROUTE WHEN NEED TO FILTER OUT??
    # print("DATES ARE NOW GROUPED:", dates_grouped_by_seven)
    # session["grouped_dates"] = dates_grouped_by_seven
    # group = session["grouped_dates"]
    # print("GROUP ME!!:", group)

    ######################

    return render_template(
        "sleep_graphs.html",
        user_id=user_id,
        sleep_log_user_obj=sleep_log_user_obj,
        converted_current_date=converted_current_date,
        dates_grouped_by_seven=dates_grouped_by_seven,
    )


# TODO LEFT OFF HERE 11/29 !!!!
# TODO picking a point on the monthly graph, display that specific date and journal info ONLY
@app.route("/month-date-only", methods=["GET", "POST"])
def display_date_info_chosen_from_month_graph():
    """Return specific date and journal info"""

    # post_date = []
    # print("THE DATE NOW IS:", post_date)
    # NOTE NOTE: SOLVED!!! THE SOLUTION NEEDED TO BE STORED IN A SESSION.
    # THis is because the .ajax on the JS side will run a POST request which will store the first date as a session. THen, the
    # window.location will execute a GET request. By then, the session is already stored and should be able to relay that info back!
    # new_date = ""
    if request.method == "POST":
        # print("THIS IS FROM THE POST SIDE OF MONTH GRAPH JS SIDE")
        # data = {}
        # data["date"] = request.json["xAxisDatapoint"]
        # data["hour"] = request.json["yAxisdatapoint"]

        # data = request.json
        # print(data)
        # print(data)
        user_id = session["user"]
        # print(request.get_json())
        data = request.get_json()  # {'information': {'date': '11/14', 'hour': 9.19}}

        # Pull date info from the nested dictionary above
        date = data["information"]["date"]
        # print(type(date))
        # print("THE DATE THAT WAS SELECTED FROM THE MONTH GRAPH WAS:", date)
        # post_date.append(date)

        # If the session is already created, then pop what was in it so that a new session can be stored
        if "post_date" in session:
            # print("YEP SOMETHING IS HERE")
            session.pop("post_date")
            # print(session["post_date"])  #SO THIS WORKS BECAUSE THERE IS NOT REGISTERED "POST DATE" AFTER THE POP happens
            session["post_date"] = date
        else:
            # If the session doesn't exist, create a session
            # print("NOPE NOTHING IS HERE")
            session["post_date"] = date

        # post_date = session["post_date"]
        datee = session.get("post_date")
        # print("DATE HERE IS:", datee)
        # print("THE POST DATE WAS:", post_date)
        # print(session["post_date"])
        # new_date = date

        return redirect("/month-date-only")

    # TODO I think I want to try returning an object that is a jsonify object. Then from there, I can target that graph

    # NOTE: Prob don't need this conditional since it is a POST request...
    # print("THE NEW DATE IS:", new_date)
    if request.method == "GET":
        # print("THIS IS FROM THE GET SIDE MONTH GRAPH JS SIDE")
        # data = {}
        # data["date"] = request.json["date"]
        # data["hour"] = request.json["hour"]
        chosen_date_str = session.get(
            "post_date"
        )  # String, has the format "11/29" example
        # post_date = session["post_date"]
        # print("THE DATE FOR THE GET SIDE SESSION IS:", chosen_date_str)
        # data = request.get_json(silent=True)

        # print("ANYTHING HERE?", data)
        # print(request.get_json())
        # data = request.get_json()

        # data_2 = request.json

        # TODO: So now that I am getting the correct selected date from the month chart. Now, take that date and filter in the crud.py for that user's id.
        user_id = session["user"]

        # ===================
        # Step 1: Query that date info from that user.
        # sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

        chosen_date_by_user_obj = datetime_functions.change_filtered_dates_different_format_to_obj(
            chosen_date_str
        )

        # print("THE CHOSEN DATE BY USER OBJ FROM STRING IS:", chosen_date_by_user_obj)

        filtered_date_obj = crud.get_sleep_data_by_filtered_date(
            user_id, chosen_date_by_user_obj
        )

        # Now use that filtered_date_obj to get the wake and bed times
        # FIXME: Include AM and PM times.
        filtered_date_wake_time_obj = filtered_date_obj.wake_time
        # print("THE DATETIME TIME OBJ FOR WAKE_TIME IS", filtered_date_obj)

        # Convert to a string to include the AM and PM
        # Cannot pass in a datetime.time object, but a datetime.date object!
        wake_time_str = str(filtered_date_wake_time_obj)
        wake_time_new_str = datetime_functions.format_time_str(wake_time_str)

        if wake_time_new_str[-2:] == "PM":
            wake_time_num_slice = int(wake_time_str[0:2]) - 12
            # print("NUMBER WAKE TIME IS:", wake_time_num_slice)

            new_wake_time_str = (
                str(wake_time_num_slice) + wake_time_str[2:5] + " " + "PM"
            )
            wake_time_new_str = new_wake_time_str

        elif wake_time_new_str[-2:] == "AM":
            wake_time_new_str = wake_time_new_str[1:]

        # ========BED TIME BELOW:
        filtered_date_bed_time_obj = filtered_date_obj.bed_time

        # filtered_date_bed_time_obj = float(filtered_date_bed_time_obj) - 12

        bed_time_str = str(filtered_date_bed_time_obj)

        # bed_time_num_slice = int(bed_time_str[0:2]) - 12
        # print("NUMBER BED TIME IS:", bed_time_num_slice)  # It is 11

        # new_bed_time_str = str(bed_time_num_slice) + bed_time_str[2:]
        # print(
        #     "THE NEW BED TIME STRING RE FORMATTED FROM MILITARY TIME IS:",
        #     new_bed_time_str,
        # )

        # bed_time_str = str(new_bed_time_str)

        bed_time_new_str = datetime_functions.format_time_str(bed_time_str)
        # print("THE BED TIME HERE IS:", bed_time_new_str)

        # NOTE: Changing the format of this string from the military time!
        if bed_time_new_str[-2:] == "PM":
            bed_time_num_slice = int(bed_time_str[0:2]) - 12
            # print("NUMBER BED TIME IS:", bed_time_num_slice)

            new_bed_time_str = str(bed_time_num_slice) + bed_time_str[2:5] + " " + "PM"
            bed_time_new_str = new_bed_time_str

        elif bed_time_new_str[-2:] == "AM":
            bed_time_new_str = bed_time_new_str[1:]

        # bed_time_new_str = int(bed_time_new_str)

        # bed_time_new_str = bed_time_new_str - 12
        # ===================================================================
        # Now, display the User's Journal based on the date that was filtered

        user_obj = crud.check_user_to_journal_id(user_id)
        # print(user_obj.journals)  # This is a list!

        journal_titles_by_date = {}
        for date in user_obj.journals:
            print(date.created_at)
            if chosen_date_by_user_obj == date.created_at:
                # print(date.created_at)
                # print("HEY IS THIS THE DATE YOU WANTED TO COMPARE TO JOURNALS!?")
                journal_titles_by_date[date.entry_name] = date.entry_details

        # print("JOURNAL TITLES ARE:", journal_titles_by_date)

        # NOTE: Write conditional to check if a journal title was created. If not, then display "No Journals Found"
        # if "date.entry_name" not in journal_titles_by_date:
        #     no_journal = "No Journal Found"

        # ===================================================================

        # Now starts the Hypnogram Route and the Doughnut Display for Chart.js
        user_timezone = session["timezone"]

        total_sleep_hours_this_day = datetime_functions.time_difference(
            user_timezone, filtered_date_wake_time_obj, filtered_date_bed_time_obj
        )

        # STORES total_sleep hours. Need to convert to minutes
        session["total_sleep_hours"] = total_sleep_hours_this_day
        total_sleep_hrs = session["total_sleep_hours"]
        # print("THE TOTAL SLEEP HOURS IS:", total_sleep_hrs)

        # print("The HYPNOGRAM SUBTRACTED TIME DIFF  is", total_sleep_hours_this_day)

        # NOTE: Call the datetime_function.py Hypnogram function!
        hypnogram_dict = datetime_functions.create_hypnogram(total_sleep_hours_this_day)

        # print("The SLEEP STAGE DICT Hypnogram is:", hypnogram_dict)

        session["hypnogram"] = hypnogram_dict

        hypnogram_info = session["hypnogram"]
        # print("The FINAL info for hypnogram is:", hypnogram_info)

        return render_template(
            "month_date_chosen.html",
            chosen_date=chosen_date_str,
            user_id=user_id,
            wake_time=wake_time_new_str,
            bed_time=bed_time_new_str,
            journal_titles_by_date=journal_titles_by_date
            # new_date=new_date,
        )  # NOTE: WHen this is indented one space in, like so, it works with the POST Request. However, the GET request is different and needs to be indented outward!


# TODO: So now that I am getting the correct selected date from the month chart. Now, take that date and filter in the crud.py for that user's id.

# @app.route("/after-month-date")
# def display_final_month_date():
#     """Return the JS routed month date request"""

#     user_id = session["user"]
#     date = session["post_date"]

#     return render_template("month_practice_again.html", user_id=user_id, date=date)

# TODO COMMENTED HERE FOR DEBUGGING 11/30 -----------------------
@app.route("/date-filter/<user_id>")
def display_chosen_sleep_date(user_id):
    """Return date information of via filter"""

    chosen_date_by_user_str = request.args.get("date-start")

    # print("THE STRING DATE IS:", chosen_date_by_user_str)

    print(
        type(chosen_date_by_user_str)
    )  # THis is a string. Must convert to datetime object

    chosen_date_by_user_obj = datetime_functions.create_filtered_date_obj(
        chosen_date_by_user_str
    )
    # print("THIS NEW DATE SHOULD BE AN OBJECT?:", chosen_date_by_user_obj)

    # print(type(chosen_date_by_user_obj))

    filtered_date_obj = crud.get_sleep_data_by_filtered_date(
        user_id, chosen_date_by_user_obj
    )

    print(
        "The DATE YOU SELECTED FILTERED OUT IS AN OBJ:", filtered_date_obj
    )  # YES IT WORKS!!!! But it is an object!!!

    # for i in filtered_date_obj:
    #     filtered_date = i.current_date

    # TODO: WRITE A CONDITIONAL STATEMENT HERE -> If filtered_date_obj is None, aka the user selected a date that doesn't exist, then return an Error message to user!
    if filtered_date_obj is None:
        # print("YEP NOTHING TO SEE HERE")
        flash("The date you selected does not exist")
        return redirect("/sleep-log")

    else:
        filtered_date = (
            filtered_date_obj.current_date
        )  # This stores the current date as an OBJECT

        # print("THE FILTERED DATE IS:", filtered_date)  # Example: 2020-11-26

        # TODO: Now, taking that filtered_date obj, you need to use that date to filter out a seven date period
        # print("The STORED SESSION DATES ARE:")
        # print(session["dates_group_obj"])
        grouped_per_week = session["dates_group_obj"]

        grouped_per_week_obj = []
        for i in grouped_per_week:
            # print("IS THIS?", i)

            # print(type(i)) #Is a String
            grouped_per_week_obj.append(
                datetime_functions.change_filtered_dates_to_obj(i)
            )

        # print(grouped_per_week_obj)

        dates_grouped_by_seven = []
        for x in range(0, len(grouped_per_week_obj), 7):
            dates_grouped_by_seven.append(grouped_per_week_obj[x : x + 7])

        # print("THE FINAL GROUPED DATES AS OBJECTS:", dates_grouped_by_seven)

        # NOTE: Now, Compare the filtered date to the list of dates and take only that list
        selected_group_dates_obj_lst = []
        for date in dates_grouped_by_seven:
            print()
            # print("IS THIS WORKING!?!?")
            if filtered_date in date:
                # print("THIS LIST THAT FILTERED OUT 7 DAYS:", date)
                selected_group_dates_obj_lst.append(date)

        print(
            "THE FINAL LIST OF DATES IS:", selected_group_dates_obj_lst
        )  # [[datetime.date(2020, 11, 22), datetime.date(2020, 11, 23), datetime.date(2020, 11, 24), datetime.date(2020, 11, 25), datetime.date(2020, 11, 26)]]
        # Store in session and take to the json route below

        converted_current_date_str = []  # This list contains ALL the dates.
        for date_lst in selected_group_dates_obj_lst:
            # print(date_lst)
            for date in date_lst:
                # print("LOOK HERE:", date)

                converted_current_date_str.append(date.strftime("%b-%d-%Y"))

        # print("THE CONVERTED DATES OBJ TO STR IS:", converted_current_date_str)

        session["final_weekly_dates"] = converted_current_date_str

        # NOTE: Next step is taking this list of objects and now looking in the database and calculating the wake and bed times again.
        # SO, in order, get a list of the wake up and bed times. Then get only the total hours from that and put it in a list. Store in a session and take to JSON route
        pre_time_sleep_log_obj = crud.get_sleep_time_by_filtered_date_lst(
            user_id, selected_group_dates_obj_lst
        )

        print(
            "SO the LIST OF OBJ FOR EACH DATE IS?:", pre_time_sleep_log_obj
        )  # [<SleepLog sleep_log_id = 22 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-22>, <SleepLog sleep_log_id = 23 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-23>, <SleepLog sleep_log_id = 24 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-24>, <SleepLog sleep_log_id = 25 wake_time = 05:55:00 bed_time = 23:42:52 current_date = 2020-11-25>, <SleepLog sleep_log_id = 26 wake_time = 08:33:00 bed_time = 12:20:21 current_date = 2020-11-26>]

        # NOTE: Now, take the query filtered list of objects above and take the wake and bed time hours and return a list of only those hours!
        # //  TODO STOPPED HERE!!!
        timezone = session["timezone"]
        # print("USER TIMEZONE CURRENTLY IS:", timezone)

        total_time_hours_lst = []
        for i in pre_time_sleep_log_obj:
            total_subtracted_hours = datetime_functions.time_difference(
                timezone, i.wake_time, i.bed_time
            )
            total_time_hours_lst.append(total_subtracted_hours)

        print(
            "BEFORE PASS INTO HTML THE TOTAL TIME HOURS ISL", total_time_hours_lst
        )  # CHECKS OUT, RETURNS: [10.19, 10.19, 10.19, 6.12, 20.12]

        session["total_weekly_hrs_json"] = total_time_hours_lst

        weekly_hours_lst = session["total_weekly_hrs_json"]
        # Calculate the average number of hours per week:
        average_hrs = datetime_functions.calculate_weekly_avg_hrs(weekly_hours_lst)
        # print("AVERAGE HOURS SLEPT PER WEEK:", average_hrs)

        return render_template(
            "sleep_dates_by_week.html",
            filtered_date=filtered_date,
            average_hrs=average_hrs,
            user_id=user_id,
        )


# FOR CHART.JS WEEKLY DATES
@app.route("/weekly-sleep-data.json")
def weekly_dates_json():
    """Return JSON dict to chart.js"""

    weekly_date_lst_obj = session["final_weekly_dates"]
    # print("FOR JSON WEEKLY DATES IS:", weekly_date_lst_obj)

    # converted_current_date_str = []  # This list contains ALL the dates.
    # for date_lst in weekly_date_lst_obj:
    #     print(date_lst)
    #     for date in date_lst:
    #         print("LOOK HERE:", date)

    #         converted_current_date_str.append(date.strftime("%b-%d-%Y"))

    # print("THE CONVERTED DATES FOR JSON IS:", converted_current_date_str)

    total_hrs = session["total_weekly_hrs_json"]
    # print("TOTAL HOURS LIST IS:", total_hrs)

    # sleep_hours_this_day.append(
    #     {
    #         "date": converted_current_date_this_day,
    #         "sleep_hours": total_sleep_hours_this_day,
    #     }
    # )
    weekly_sleep_data = {
        "total_hours": total_hrs,
        "dates_over_time": weekly_date_lst_obj,
    }

    return jsonify({"data": weekly_sleep_data})

    # hynogram_doughnut_data = {


#         "sleep_labels": sleep_labels,
#         "time_data": time_data,
#         "doughnut_name": doughnut_name_lst,
#         "doughnut_percent": doughnut_percent_lst,
#     }
#     return jsonify({"data": hynogram_doughnut_data})

#     # return jsonify({"data": hypnogram_data})


# This Route shows the Week depending on what User clicks on; DOESN"T WORK SINCE DATES CANNOT BE PASSED AS A LIST FROM HTML TO BACKEND!
# @app.route("/data-by-weekly-dates/<user_id>/<dates>")
# def display_weekly_dates(user_id, dates):
#     """Return graph of sleep dates per selected week interval"""

#     print("THE WEEKLY DATES USER SELECTED ARE:")

#     return render_template("sleep_dates_by_week.html")

# TODO STOPPED HERE: 11/28 !!!!!!!!!!!!!
# =======================This starts the Filtering out by Month!
@app.route("/month-filter/<user_id>")
def filter_by_month(user_id):
    """Return dates by month"""

    chosen_month_by_user_str = request.args.get("start-month")  # 2020-11 (STRING)

    # print("THE CHOSEN MONTH BY USER WAS:", chosen_month_by_user_str)

    sleep_log_user_obj = crud.get_sleep_data_user_id(
        user_id
    )  # <User user_id = 1 first_name = Shelby>

    # print("ALL THE USER'S  DATA IS:", sleep_log_user_obj)

    # Now I need to call the joined sleep_log table
    all_date_obj_lst = []
    for data in sleep_log_user_obj.sleep_logs:
        print(data.current_date)  # 2020-11-25
        print(type(data.current_date))  # <class 'datetime.date'>
        # print(data.current_date[0]) #ERROR! NOT SCRIPTABLE
        all_date_obj_lst.append(data.current_date)

    print(
        "LIST OF ALL DATE OBJECTS IS:", all_date_obj_lst
    )  # [datetime.date(2020, 11, 1), datetime.date(2020, 11, 2), datetime.date(2020, 11, 3), datetime.date(2020, 11, 4), datetime.date(2020, 11, 5), datetime.date(2020, 11, 6), datetime.date(2020, 11, 7), datetime.date(2020, 11, 8), datetime.date(2020, 11, 9), datetime.date(2020, 11, 10), datetime.date(2020, 11, 11), datetime.date(2020, 11, 12), datetime.date(2020, 11, 13), datetime.date(2020, 11, 14), datetime.date(2020, 11, 15), datetime.date(2020, 11, 16), datetime.date(2020, 11, 17), datetime.date(2020, 11, 18), datetime.date(2020, 11, 19), datetime.date(2020, 11, 20), datetime.date(2020, 11, 21), datetime.date(2020, 11, 22), datetime.date(2020, 11, 23), datetime.date(2020, 11, 24), datetime.date(2020, 11, 25), datetime.date(2020, 11, 26), datetime.date(2020, 11, 27)]
    ##############
    # I Can do The following steps:
    # 1. Store the datetime in a list
    # 2. Convert that list to a string format with only the 2020-11 present
    ##############
    all_datetime_str_lst = datetime_functions.create_date_str(all_date_obj_lst)
    print(
        "ALL DATES AS A STRING IS:", all_datetime_str_lst
    )  # ['2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11', '2020-11']

    # NOW, need to take the all_date_obj_lst and convert to the converted string dates "2020-11-1"
    converted_dates_obj_to_str = datetime_functions.convert_date_obj_to_str_format(
        all_date_obj_lst
    )

    print(
        "IF YOU MAKE IT HERE THE ALL STRINGS DATES ARE:", converted_dates_obj_to_str
    )  # ['2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27']

    # Now combine the converted string dates and the HTML selected month dates into a dict:
    all_month_dict = {
        converted_dates_obj_to_str[i]: all_datetime_str_lst[i]
        for i in range(len(converted_dates_obj_to_str))
    }

    print(
        "THE DICTIONARY FOR MONTHS IS:", all_month_dict
    )  # {'2020-11-01': '2020-11', '2020-11-02': '2020-11', '2020-11-03': '2020-11', '2020-11-04': '2020-11', '2020-11-05': '2020-11', '2020-11-06': '2020-11', '2020-11-07': '2020-11', '2020-11-08': '2020-11', '2020-11-09': '2020-11', '2020-11-10': '2020-11', '2020-11-11': '2020-11', '2020-11-12': '2020-11', '2020-11-13': '2020-11', '2020-11-14': '2020-11', '2020-11-15': '2020-11', '2020-11-16': '2020-11', '2020-11-17': '2020-11', '2020-11-18': '2020-11', '2020-11-19': '2020-11', '2020-11-20': '2020-11', '2020-11-21': '2020-11', '2020-11-22': '2020-11', '2020-11-23': '2020-11', '2020-11-24': '2020-11', '2020-11-25': '2020-11', '2020-11-26': '2020-11', '2020-11-27': '2020-11'}

    # Now return only the selected months and string dates associated with tht HTML choosen date values from the dict and RETURN a new list with those months
    selected_month_filter_str_lst = []

    for k, v in all_month_dict.items():
        if v == chosen_month_by_user_str:
            selected_month_filter_str_lst.append(k)

    print(
        "Filtered OUT MONTHS FROM CHOSEN HTML DATE ARE:", selected_month_filter_str_lst
    )  # ['2020-11-01', '2020-11-02', '2020-11-03', '2020-11-04', '2020-11-05', '2020-11-06', '2020-11-07', '2020-11-08', '2020-11-09', '2020-11-10', '2020-11-11', '2020-11-12', '2020-11-13', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-17', '2020-11-18', '2020-11-19', '2020-11-20', '2020-11-21', '2020-11-22', '2020-11-23', '2020-11-24', '2020-11-25', '2020-11-26', '2020-11-27']

    # TODO FINISH HERE 11/28 !!!!!
    # Now take that list of strings and convert back to datetime.date obj. Then do a crud filter for those objects and get the wake,bed time info. Look above on line 476 for how to do it with the last grouped dates!

    month_date_obj_lst = datetime_functions.create_filtered_date_obj_from_str_lst(
        selected_month_filter_str_lst
    )

    print(
        "CONVERTED MONTHS FROM STR TO OBJ LST:", month_date_obj_lst
    )  # [datetime.datetime(2020, 11, 1, 0, 0), datetime.datetime(2020, 11, 2, 0, 0), datetime.datetime(2020, 11, 3, 0, 0), datetime.datetime(2020, 11, 4, 0, 0), datetime.datetime(2020, 11, 5, 0, 0), datetime.datetime(2020, 11, 6, 0, 0), datetime.datetime(2020, 11, 7, 0, 0), datetime.datetime(2020, 11, 8, 0, 0), datetime.datetime(2020, 11, 9, 0, 0), datetime.datetime(2020, 11, 10, 0, 0), datetime.datetime(2020, 11, 11, 0, 0), datetime.datetime(2020, 11, 12, 0, 0), datetime.datetime(2020, 11, 13, 0, 0), datetime.datetime(2020, 11, 14, 0, 0), datetime.datetime(2020, 11, 15, 0, 0), datetime.datetime(2020, 11, 16, 0, 0), datetime.datetime(2020, 11, 17, 0, 0), datetime.datetime(2020, 11, 18, 0, 0), datetime.datetime(2020, 11, 19, 0, 0), datetime.datetime(2020, 11, 20, 0, 0), datetime.datetime(2020, 11, 21, 0, 0), datetime.datetime(2020, 11, 22, 0, 0), datetime.datetime(2020, 11, 23, 0, 0), datetime.datetime(2020, 11, 24, 0, 0), datetime.datetime(2020, 11, 25, 0, 0), datetime.datetime(2020, 11, 26, 0, 0), datetime.datetime(2020, 11, 27, 0, 0)]

    # Now take the list of datetime.date objects and do a query filter to get the wake and bed times
    user_sleep_log_obj_for_date_lst = crud.get_sleep_time_by_filtered_month_lst(
        user_id, month_date_obj_lst
    )

    print(
        "USER OBJ WITH THOSE FILTERED DATE MONTHS:", user_sleep_log_obj_for_date_lst
    )  # [<SleepLog sleep_log_id = 1 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-01>, <SleepLog sleep_log_id = 2 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-02>, <SleepLog sleep_log_id = 3 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-03>, <SleepLog sleep_log_id = 4 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-04>, <SleepLog sleep_log_id = 5 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-05>, <SleepLog sleep_log_id = 6 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-06>, <SleepLog sleep_log_id = 7 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-07>, <SleepLog sleep_log_id = 8 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-08>, <SleepLog sleep_log_id = 9 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-09>, <SleepLog sleep_log_id = 10 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-10>, <SleepLog sleep_log_id = 11 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-11>, <SleepLog sleep_log_id = 12 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-12>, <SleepLog sleep_log_id = 13 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-13>, <SleepLog sleep_log_id = 14 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-14>, <SleepLog sleep_log_id = 15 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-15>, <SleepLog sleep_log_id = 16 wake_time = 08:30:00 bed_time = 23:11:00 current_date = 2020-11-16>, <SleepLog sleep_log_id = 17 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-17>, <SleepLog sleep_log_id = 18 wake_time = 10:30:00 bed_time = 23:11:00 current_date = 2020-11-18>, <SleepLog sleep_log_id = 19 wake_time = 07:30:00 bed_time = 23:11:00 current_date = 2020-11-19>, <SleepLog sleep_log_id = 20 wake_time = 10:30:00 bed_time = 23:11:00 current_date = 2020-11-20>, <SleepLog sleep_log_id = 21 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-21>, <SleepLog sleep_log_id = 22 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-22>, <SleepLog sleep_log_id = 23 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-23>, <SleepLog sleep_log_id = 24 wake_time = 09:30:00 bed_time = 23:11:00 current_date = 2020-11-24>, <SleepLog sleep_log_id = 25 wake_time = 05:55:00 bed_time = 23:42:52 current_date = 2020-11-25>, <SleepLog sleep_log_id = 26 wake_time = 08:33:00 bed_time = 12:20:21 current_date = 2020-11-26>, <SleepLog sleep_log_id = 27 wake_time = 06:30:00 bed_time = 17:55:33 current_date = 2020-11-27>]

    timezone = session["timezone"]
    # print("USER TIMEZONE CURRENTLY IS:", timezone)

    total_time_hours_lst = []
    for i in user_sleep_log_obj_for_date_lst:
        total_subtracted_hours = datetime_functions.time_difference(
            timezone, i.wake_time, i.bed_time
        )
        total_time_hours_lst.append(total_subtracted_hours)

    print(
        "THE TOTAL TIME HOURS IS", total_time_hours_lst
    )  # [8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 8.19, 9.19, 10.19, 11.19, 8.19, 11.19, 10.19, 10.19, 10.19, 10.19, 6.12, 20.12, 12.34]

    # Now convert the datetime obj list to formatted strings to be displayed to the front end!
    #   1. Will pick two displays: Currently We have: Nov 1 (looks cluttered)
    #   2. 11/1/20
    #   3/ 11/1

    # Type string format #1:
    month_date_converted_to_str = datetime_functions.create_date_str_with_different_format(
        month_date_obj_lst
    )

    print(
        "THE FIRST TYPE:", month_date_converted_to_str
    )  # ['11/01', '11/02', '11/03', '11/04', '11/05', '11/06', '11/07', '11/08', '11/09', '11/10', '11/11', '11/12', '11/13', '11/14', '11/15', '11/16', '11/17', '11/18', '11/19', '11/20', '11/21', '11/22', '11/23', '11/24', '11/25', '11/26', '11/27', '11/28']

    # NOW STORE TIME HOURS AND MONTHS STRINGS INTO A SESSION AND PUT INTO A JSON ROUTE
    session["month_total_hours"] = total_time_hours_lst
    session["month_dates"] = month_date_converted_to_str

    return render_template(
        "sleep_log_by_month.html",
        user_id=user_id,
        chosen_month_by_user_str=chosen_month_by_user_str,
    )


@app.route("/monthly-sleep-data.json")
def monthly_dates_json():
    """Return JSON dict with a month dates to chart.js"""

    total_monthly_hours = session["month_total_hours"]
    # print("FOR JSON MONTH ROUTE THE TOTAL MONTHLY HOURS IS:", total_monthly_hours)

    all_dates_in_month = session["month_dates"]
    # print("MONTHLY DATES FOR CHOSEN DATE IS:", all_dates_in_month)

    monthly_sleep_data = {
        "total_monthly_hours": total_monthly_hours,
        "monthly_dates_over_time": all_dates_in_month,
    }

    return jsonify({"data": monthly_sleep_data})


# TODO COMMENTED OUT HERE FOR DEBUGGING!!!!!!!!!!!!!!! WILL NEED TO RE-COMMENT!!!

# FIXME NOTE: This function is kinda DRY...bit repetitive from the one above
@app.route("/sleep-data-by-date/<user_id>/<date>")
def display_sleep_times_for_date(user_id, date):
    """Return sleep wake and bed time page"""

    print(
        "THE HTML DATE is:", date
    )  # NOTE: ThIS CHECKS OUT! The date does pass in correctly depending on what the user click on

    # print(type(date))

    date_obj = datetime_functions.create_date_obj(date)
    # print("The NEW DATETIME DATE Object is:", date_obj)

    user_id = session["user"]
    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    # print("The user object is:", sleep_log_user_obj)

    # TODO: MAKE A CRUD FUNCTION THAT CHECKS THE DATE IN THE DATABASE!! QUERY FOR IT! NOTE: Nvm...cannot filter by Date because need to filter by user_id since multiple dates in that database!
    # sleep_log_current_date_obj = crud.get_sleep_data_by_date(date)
    # print("The CURRENT DATE is", sleep_log_current_date_obj)
    current_date_lst = []
    for date in sleep_log_user_obj.sleep_logs:
        # print("DOES THIS WORK?", date.current_date)
        current_date_lst.append(date.current_date)

    print(
        current_date_lst
    )  # NOTE: CHECKING if works; IT IS, but it is now a list of datetime.date objects! Not the previous formatted string

    # // TODO: CHECKING HERE IF the HTML "date" is the date the user clicked on!
    # NOTE: This conditional isn't even running because the "date" is != to the datetime objects in that list
    # SO I can either convert this "date" string into an object to compare to the list of objects
    # print()
    # print("CHECK THIS NOW!!!")
    # NOTE: Convert the datetime.datetime obj to a datetime.date ONLY object

    # if date_obj in current_date_lst:
    #     print(
    #         "The DATE OBJECT matches the dates in list:", date_obj
    #     )  # UPDATE: IT WORKS!

    #     correct_date_obj = date_obj
    #     print("The CORRECT DATE obj is:", correct_date_obj)
    # // TODO: Making the "date" HTML string into a datetime.date object

    # // TODO:THIS FUNCTION IS NOT CATCHING THE RIGHT DATE!
    wake_bed_times_obj = crud.get_sleep_data_by_date(
        user_id, current_date_lst, date_obj
    )
    # print("IF THIS WORKS", wake_bed_times_obj)

    unconverted_current_date = wake_bed_times_obj.current_date
    # NOTE: Going to put this datetime object into a session (This is unformatted version!!)
    session["datetime_object_current_date"] = unconverted_current_date

    converted_current_date = unconverted_current_date.strftime("%b-%d-%Y")

    # NOTE: Get the total sleep hours by getting the time difference function from datetime_functions.py
    # total_sleep_hours = datetime_functions.time_difference

    # ===============================DISPLAYING USER JOURNAL BASED ON DATE
    print()
    user_obj = crud.check_user_to_journal_id(user_id)
    # print("THIS ROUTE IS THE SLEEP-JOURNAL ROUTE")
    print()

    # print("The user_obj is:", user_obj)
    print(user_obj.journals)  # This is a list!

    # TODO FIXMEEEEEEEE; update: IT CHECKS OUT!!! IT WORKS! I CAN PASS IN A DICTIONARY!! TO JINJA
    journal_titles_by_date = {}
    for date in user_obj.journals:
        print(date.created_at)
        if unconverted_current_date == date.created_at:
            print(date.created_at)
            # print("HEY IS THIS THE DATE YOU WANTED TO COMPARE TO JOURNALS!?")
            journal_titles_by_date[date.entry_name] = date.entry_details

    # print("JOURNAL TITLES ARE:", journal_titles_by_date)

    return render_template(
        "sleep_bed_wake_times.html",
        user_id=user_id,
        converted_current_date=converted_current_date,
        sleep_log_user_obj=sleep_log_user_obj,
        wake_bed_times_obj=wake_bed_times_obj,
        journal_titles_by_date=journal_titles_by_date,
    )


# ===================================================
# THIS ROUTE READS THE JOURNALS IF USER CLICKS ON THEM!
@app.route("/journal-entries/<entry_details>")
def read_journals(entry_details):
    # print("WHAT IS THIS ENTRY???:", entry_details)

    return render_template("choosen_journal_details.html", entry_details=entry_details)


# ===================================================


@app.route("/total-sleep.json")
def get_total_sleep():
    """Get total sleep per day"""

    user_id = session["user"]
    # print("FOR TOTAL SLEEP JSON user is:", user_id)
    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    # NOTE: Need to convert the date to this format in this file, not the crud file because you'll still get this output to frontend: 2020-11-13 00:00:00, which is not what I need. Just the date, not the time
    sleep_hours_this_day = []
    for date in sleep_log_user_obj.sleep_logs:
        # print("The date in the database is", date.current_date)
        # print("The session current date is", session["current_date"])  #FIXME NOTE: somehow, after commenting this out, the session error that current data doesn't exist anymore works!
        # if date.current_date == session["current_date"]:
        current_date = date.current_date
        converted_current_date_this_day = current_date.strftime("%b-%d-%Y")

        # print("The CURRENT CONVERTED Date is", converted_current_date_this_day)

        # print("The WAKE time is", date.wake_time)
        # print("The BED time is", date.bed_time)

        # Calling the user's timezone from session
        user_timezone = session["timezone"]

        total_sleep_hours_this_day = datetime_functions.time_difference(
            user_timezone, date.wake_time, date.bed_time
        )

        # print("The SUBTRACTED TIME DIFF is", total_sleep_hours_this_day)

        sleep_hours_this_day.append(
            {
                "date": converted_current_date_this_day,
                "sleep_hours": total_sleep_hours_this_day,
            }
        )

    return jsonify({"data": sleep_hours_this_day})


# =======
# Hypnogram JSON Route Happens Chart.JS

# FIXME: MIGHT NOT NEED THIS ROUTE ANYMORE!!!! COMMENT OUT FOR NOW 11/30
# @app.route("/hypnogram/<user_id>/<selected_date>/<wake_time>/<bed_time>")
# def create_hypnogram(user_id, selected_date, wake_time, bed_time):
#     """Return hypnogram graph"""

#     # NOTE: Just to Check; Delete later
#     print("The USER ID for this path is:", user_id)
#     print("The CURRENT SELECTED DATE path is:", selected_date)
#     print("The WAKE TIME path is:", wake_time)
#     print("The BED TIME path is:", bed_time)

#     user_timezone = session["timezone"]

#     total_sleep_hours_this_day = datetime_functions.time_difference(
#         user_timezone, wake_time, bed_time
#     )

#     # STORES total_sleep hours. Need to convert to minutes
#     session["total_sleep_hours"] = total_sleep_hours_this_day
#     total_sleep_hrs = session["total_sleep_hours"]
#     print("THE TOTAL SLEEP HOURS IS:", total_sleep_hrs)

#     print("The HYPNOGRAM SUBTRACTED TIME DIFF  is", total_sleep_hours_this_day)

#     # NOTE: Call the datetime_function.py Hypnogram function!
#     hypnogram_dict = datetime_functions.create_hypnogram(total_sleep_hours_this_day)

#     print("The SLEEP STAGE DICT Hypnogram is:", hypnogram_dict)

#     session["hypnogram"] = hypnogram_dict

#     hypnogram_info = session["hypnogram"]
#     print("The FINAL info for hypnogram is:", hypnogram_info)

#     return render_template(
#         "hypnogram.html",
#         user_id=user_id,
#         selected_date=selected_date,
#         wake_time=wake_time,
#         bed_time=bed_time,
#     )


@app.route("/hypnogram-sleep.json")
def get_individual_sleep_times():
    """Get total sleep per day and Return JSON dictionary for Chart.js"""

    total_sleep_hrs = session["total_sleep_hours"]
    # print("Total SLEEP HOURS for JSON route is:", total_sleep_hrs)

    total_sleep_min = total_sleep_hrs * 60

    hypnogram_time_dict = session["hypnogram"]  # Return time_dict
    # print("THE Hypnogram SLEEP JSON route time_dict is:", hypnogram_time_dict)

    # NOTE: need to put the sleep stages as individual units on y axis
    # sleep_stages = []
    # for each_stage in hypnogram_info.keys():
    #     sleep_stages.append(each_stage)

    # print("The SLEEP STAGES for JSON is:", sleep_stages)

    # # NOTE: need to put the time for each stages for x axis
    # time_stages = []
    # for time in hypnogram_info.values():
    #     time_stages.append(time)

    # print("The TIME STAGES for JSON is:", time_stages)

    # =========================================================
    time_stages = datetime_functions.create_time_stages(
        hypnogram_time_dict, total_sleep_hrs
    )

    # print("THE TIME STAGE ON SERVER.PY side is:", time_stages)

    time_lst = datetime_functions.create_total_time_lst(time_stages)

    # print("The TIME LST on SERVER.PY side is", time_lst)

    final_time_dict = datetime_functions.create_time_final_dict(
        time_stages, time_lst, total_sleep_hrs
    )
    # print("DOES FINAL time dict work?:", final_time_dict)
    # =========================================================
    # hypnogram_data = []

    # for time_stage, sleep_stage in final_time_dict.items():

    #     hypnogram_data.append(
    #         {"sleep_mins": time_stage, "sleep_stages": sleep_stage,}
    #     )

    # print("The data going INTO Chart.js Hypnogram is:", hypnogram_data)

    # CHART.JS Hypnogram==================
    sleep_labels = [0]
    time_data = [0]
    for key_time, value_stage in final_time_dict.items():
        time_data.append(key_time)
        sleep_labels.append(value_stage)

    # // TODO: There is a bug where the time added is wrong. Example, 9.19 hrs for Nov 16th is about 551.4min, however, it returns over 630min. No problem with function in Sublime
    print()
    print("THE LABELS for Hynogram is:", sleep_labels)
    print("THE DATA for hynoogram is:", time_data)
    print()

    # return jsonify(labels, data)  #Returning object

    # CHART.JS Doughnut======================

    doughnut_data_dict = datetime_functions.create_doughnut_chart(
        hypnogram_time_dict, total_sleep_min
    )

    print()
    # print("THE Data from the DOUGHNUT dict is:", doughnut_data_dict)
    print()

    doughnut_percent_lst = []
    doughnut_name_lst = []

    for sleep_name, percentage in doughnut_data_dict.items():
        doughnut_name_lst.append(sleep_name)
        doughnut_percent_lst.append(f"{percentage:.2f}")

    # print("The DOUGHNUT percents is:", doughnut_percent_lst)
    # print("The DOUGHNUT Name is:", doughnut_name_lst)

    # doughnut_data_lst = []
    # awake_percentage = doughnut_data_dict.get("Awake")
    # awake_percentage_formatted = "{:.2f}".format(awake_percentage)
    # print("The AWAKE PERCENTAGE IS:", awake_percentage_formatted)

    # light_sleep_percentage = doughnut_data_dict.get("Light Sleep")
    # light_sleep_percentage_formatted = "{:.2f}".format(light_sleep_percentage)

    # deep_sleep_percentage = doughnut_data_dict.get("Deep Sleep")
    # deep_sleep_percentage_formatted = "{:.2f}".format(deep_sleep_percentage)

    # rem_sleep_percentage = doughnut_data_dict.get("REM Sleep")
    # rem_sleep_percentage_formatted = "{:.2f}".format(rem_sleep_percentage)

    hynogram_doughnut_data = {
        "sleep_labels": sleep_labels,
        "time_data": time_data,
        "doughnut_name": doughnut_name_lst,
        "doughnut_percent": doughnut_percent_lst,
    }
    return jsonify({"data": hynogram_doughnut_data})

    # return jsonify({"data": hypnogram_data})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
