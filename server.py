"""Server for Sleep app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import crud
import datetime_functions
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
        flash("Logged in!")

        # NOTE: Storing user primary id in a session
        session["user"] = user_details.user_id
        print(session["user"])

        # NOTE: Storing user's timezone in a session
        session["timezone"] = user_details.timezone
        print(session["timezone"])

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

    print()
    print("USER OBJECT IS FROM JOURNAL:", user_obj)
    print()

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

    timezone = session["timezone"]
    created_at = datetime_functions.current_date_timezone_from_utc(timezone)
    updated_at = datetime_functions.current_date_timezone_from_utc(timezone)

    print()
    print("The CREATED TIME AT:", created_at)
    print("The Updated time is:", updated_at)
    print()
    # if user_id matches True:
    crud.create_journal_entry(
        user_id, entry_name, entry_details, created_at, updated_at
    )
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
    print("The HTML type WAKE time is:", type(wake_time))
    # COnvert to H:M:S by adding a ":00" string

    wake_add_sec_time = ":00"
    wake_time = wake_time + wake_add_sec_time
    print("THE Wake_time from the alarm is NOWL", wake_time)

    # NOTE: bed time calculation done by taking in user's current time zone from session
    user_timezone = session["timezone"]
    print(user_timezone)  # FIXME: Just a check

    bed_time = datetime_functions.current_time_timezone_from_utc(user_timezone)
    print(bed_time)  # FIXME: Just a check, This is a STRING formatted
    print("The HTML type BED time is:", type(bed_time))

    # NOTE: current_date calculation based on timezone because before, the date was not aware
    current_date = datetime_functions.current_date_timezone_from_utc(user_timezone)
    print(current_date)  # FIXME: This is a just a check
    session[
        "current_date"
    ] = current_date  # NOTE: This is NOT the converted datetime format, just the regular object non formated??????
    print("The SESSION STORED is", session["current_date"])  # Just an datetime object!

    # Seed into the database what user choose for wake time
    crud.create_sleep_log(user_id, wake_time, bed_time, current_date)
    print("THE NEXT STEP IS")

    # Find the total time user will have from bed time to wake time:
    user_total_time = datetime_functions.time_difference(
        user_timezone, wake_time, bed_time
    )

    print("The Calculated SUBTRACT TIME is", user_total_time)
    flash("Your alarm is set")

    return redirect("/sleep-log")


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

    print("CONVERTED CURRENT DATE LIST IS:", converted_current_date_for_grouping_obj)

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


@app.route("/date-filter/<user_id>")
def display_chosen_sleep_date(user_id):
    """Return date information of via filter"""

    chosen_date_by_user_str = request.args.get("date-start")

    print("THE STRING DATE IS:", chosen_date_by_user_str)

    print(
        type(chosen_date_by_user_str)
    )  # THis is a string. Must convert to datetime object

    chosen_date_by_user_obj = datetime_functions.create_filtered_date_obj(
        chosen_date_by_user_str
    )
    print("THIS NEW DATE SHOULD BE AN OBJECT?:", chosen_date_by_user_obj)

    filtered_date_obj = crud.get_sleep_data_by_filtered_date(
        user_id, chosen_date_by_user_obj
    )

    print(
        "The DATE YOU SELECTED FILTERED OUT IS AN OBJ:", filtered_date_obj
    )  # YES IT WORKS!!!! But it is an object!!!

    # for i in filtered_date_obj:
    #     filtered_date = i.current_date

    filtered_date = (
        filtered_date_obj.current_date
    )  # This stores the current date as an OBJECT

    print("THE FILTERED DATE IS:", filtered_date)  # Example: 2020-11-26

    # TODO: Now, taking that filtered_date obj, you need to use that date to filter out a seven date period
    print("The STORED SESSION DATES ARE:")
    print(session["dates_group_obj"])
    grouped_per_week = session["dates_group_obj"]

    grouped_per_week_obj = []
    for i in grouped_per_week:
        # print("IS THIS?", i)

        # print(type(i)) #Is a String
        grouped_per_week_obj.append(datetime_functions.change_filtered_dates_to_obj(i))

    print(grouped_per_week_obj)

    dates_grouped_by_seven = []
    for x in range(0, len(grouped_per_week_obj), 7):
        dates_grouped_by_seven.append(grouped_per_week_obj[x : x + 7])

    print("THE FINAL GROUPED DATES AS OBJECTS:", dates_grouped_by_seven)

    # NOTE: Now, Compare the filtered date to the list of dates and take only that list
    selected_group_dates_obj_lst = []
    for date in dates_grouped_by_seven:
        print()
        print("IS THIS WORKING!?!?")
        if filtered_date in date:
            print("THIS LIST THAT FILTERED OUT 7 DAYS:", date)
            selected_group_dates_obj_lst.append(date)

    print("THE FINAL LIST OF DATES IS:", selected_group_dates_obj_lst)
    # Store in session and take to the json route below
    session["final_weekly_dates"] = selected_group_dates_obj_lst

    # NOTE: Next step is taking this list of objects and now looking in the database and calculating the wake and bed times again.
    # SO, in order, get a list of the wake up and bed times. Then get only the total hours from that and put it in a list. Store in a session and take to JSON route
    pre_time_sleep_log_obj = crud.get_sleep_time_by_filtered_date_lst(
        user_id, selected_group_dates_obj_lst
    )

    print("SO the LIST OF OBJ FOR EACH DATE IS?:", pre_time_sleep_log_obj)

    # NOTE: Now, take the query filtered list of objects above and take the wake and bed time hours and return a list of only those hours!

    return render_template("sleep_dates_by_week.html", filtered_date=filtered_date)


# FOR CHART.JS WEEKLY DATES
@app.route("/weekly-sleep-data.json")
def weekly_dates_json():
    """Return JSON dict to chart.js"""

    weekly_date_list_obj = session["final_weekly_dates"]
    print("FOR JSON WEEKLY DATES IS:", weekly_date_list_obj)

    # sleep_hours_this_day.append(
    #     {
    #         "date": converted_current_date_this_day,
    #         "sleep_hours": total_sleep_hours_this_day,
    #     }
    # )

    # return jsonify({"data": sleep_hours_this_day})


# This Route shows the Week depending on what User clicks on; DOESN"T WORK SINCE DATES CANNOT BE PASSED AS A LIST FROM HTML TO BACKEND!
# @app.route("/data-by-weekly-dates/<user_id>/<dates>")
# def display_weekly_dates(user_id, dates):
#     """Return graph of sleep dates per selected week interval"""

#     print("THE WEEKLY DATES USER SELECTED ARE:")

#     return render_template("sleep_dates_by_week.html")


# TODO COMMENTED OUT HERE FOR DEBUGGING!!!!!!!!!!!!!!! WILL NEED TO RE-COMMENT!!!

# # FIXME NOTE: This function is kinda DRY...bit repetitive from the one above
# @app.route("/sleep-data-by-date/<user_id>/<date>")
# def display_sleep_times_for_date(user_id, date):
#     """Return sleep wake and bed time page"""

#     print(
#         "THE HTML DATE is:", date
#     )  # NOTE: ThIS CHECKS OUT! The date does pass in correctly depending on what the user click on

#     print(type(date))

#     date_obj = datetime_functions.create_date_obj(date)
#     print("The NEW DATETIME DATE Object is:", date_obj)

#     user_id = session["user"]
#     sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

#     print("The user object is:", sleep_log_user_obj)

#     # TODO: MAKE A CRUD FUNCTION THAT CHECKS THE DATE IN THE DATABASE!! QUERY FOR IT! NOTE: Nvm...cannot filter by Date because need to filter by user_id since multiple dates in that database!
#     # sleep_log_current_date_obj = crud.get_sleep_data_by_date(date)
#     # print("The CURRENT DATE is", sleep_log_current_date_obj)
#     current_date_lst = []
#     for date in sleep_log_user_obj.sleep_logs:
#         print("DOES THIS WORK?", date.current_date)
#         current_date_lst.append(date.current_date)

#     print(
#         current_date_lst
#     )  # NOTE: CHECKING if works; IT IS, but it is now a list of datetime.date objects! Not the previous formatted string

#     # // TODO: CHECKING HERE IF the HTML "date" is the date the user clicked on!
#     # NOTE: This conditional isn't even running because the "date" is != to the datetime objects in that list
#     # SO I can either convert this "date" string into an object to compare to the list of objects
#     print()
#     print("CHECK THIS NOW!!!")
#     # NOTE: Convert the datetime.datetime obj to a datetime.date ONLY object

#     # if date_obj in current_date_lst:
#     #     print(
#     #         "The DATE OBJECT matches the dates in list:", date_obj
#     #     )  # UPDATE: IT WORKS!

#     #     correct_date_obj = date_obj
#     #     print("The CORRECT DATE obj is:", correct_date_obj)
#     # // TODO: Making the "date" HTML string into a datetime.date object

#     # // TODO:THIS FUNCTION IS NOT CATCHING THE RIGHT DATE!
#     wake_bed_times_obj = crud.get_sleep_data_by_date(
#         user_id, current_date_lst, date_obj
#     )
#     print("IF THIS WORKS", wake_bed_times_obj)

#     unconverted_current_date = wake_bed_times_obj.current_date
#     # NOTE: Going to put this datetime object into a session (This is unformatted version!!)
#     session["datetime_object_current_date"] = unconverted_current_date

#     converted_current_date = unconverted_current_date.strftime("%b-%d-%Y")

#     # NOTE: Get the total sleep hours by getting the time difference function from datetime_functions.py
#     # total_sleep_hours = datetime_functions.time_difference

#     # ===============================DISPLAYING USER JOURNAL BASED ON DATE
#     print()
#     user_obj = crud.check_user_to_journal_id(user_id)
#     print("THIS ROUTE IS THE SLEEP-JOURNAL ROUTE")
#     print()

#     print("The user_obj is:", user_obj)
#     print(user_obj.journals)  # This is a list!

#     # TODO FIXMEEEEEEEE; update: IT CHECKS OUT!!! IT WORKS! I CAN PASS IN A DICTIONARY!! TO JINJA
#     journal_titles_by_date = {}
#     for date in user_obj.journals:
#         print(date.created_at)
#         if unconverted_current_date == date.created_at:
#             print(date.created_at)
#             print("HEY IS THIS THE DATE YOU WANTED TO COMPARE TO JOURNALS!?")
#             journal_titles_by_date[date.entry_name] = date.entry_details

#     print("JOURNAL TITLES ARE:", journal_titles_by_date)

#     return render_template(
#         "sleep_bed_wake_times.html",
#         user_id=user_id,
#         converted_current_date=converted_current_date,
#         sleep_log_user_obj=sleep_log_user_obj,
#         wake_bed_times_obj=wake_bed_times_obj,
#         journal_titles_by_date=journal_titles_by_date,
#     )


# # ===================================================
# # THIS ROUTE READS THE JOURNALS IF USER CLICKS ON THEM!
# @app.route("/journal-entries/<entry_details>")
# def read_journals(entry_details):
#     print("WHAT IS THIS ENTRY???:", entry_details)

#     return render_template("choosen_journal_details.html", entry_details=entry_details)


# # ===================================================


# @app.route("/total-sleep.json")
# def get_total_sleep():
#     """Get total sleep per day"""

#     user_id = session["user"]
#     print("FOR TOTAL SLEEP JSON user is:", user_id)
#     sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

#     # NOTE: Need to convert the date to this format in this file, not the crud file because you'll still get this output to frontend: 2020-11-13 00:00:00, which is not what I need. Just the date, not the time
#     sleep_hours_this_day = []
#     for date in sleep_log_user_obj.sleep_logs:
#         print("The date in the database is", date.current_date)
#         # print("The session current date is", session["current_date"])  #FIXME NOTE: somehow, after commenting this out, the session error that current data doesn't exist anymore works!
#         # if date.current_date == session["current_date"]:
#         current_date = date.current_date
#         converted_current_date_this_day = current_date.strftime("%b-%d-%Y")

#         print("The CURRENT CONVERTED Date is", converted_current_date_this_day)

#         print("The WAKE time is", date.wake_time)
#         print("The BED time is", date.bed_time)

#         # Calling the user's timezone from session
#         user_timezone = session["timezone"]

#         total_sleep_hours_this_day = datetime_functions.time_difference(
#             user_timezone, date.wake_time, date.bed_time
#         )

#         print("The SUBTRACTED TIME DIFF is", total_sleep_hours_this_day)

#         sleep_hours_this_day.append(
#             {
#                 "date": converted_current_date_this_day,
#                 "sleep_hours": total_sleep_hours_this_day,
#             }
#         )

#     return jsonify({"data": sleep_hours_this_day})


# # =======
# # Hypnogram JSON Route Happens Chart.JS


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


# @app.route("/hypnogram-sleep.json")
# def get_individual_sleep_times():
#     """Get total sleep per day and Return JSON dictionary for Chart.js"""

#     total_sleep_hrs = session["total_sleep_hours"]
#     print("Total SLEEP HOURS for JSON route is:", total_sleep_hrs)

#     total_sleep_min = total_sleep_hrs * 60

#     hypnogram_time_dict = session["hypnogram"]  # Return time_dict
#     print("THE Hypnogram SLEEP JSON route time_dict is:", hypnogram_time_dict)

#     # NOTE: need to put the sleep stages as individual units on y axis
#     # sleep_stages = []
#     # for each_stage in hypnogram_info.keys():
#     #     sleep_stages.append(each_stage)

#     # print("The SLEEP STAGES for JSON is:", sleep_stages)

#     # # NOTE: need to put the time for each stages for x axis
#     # time_stages = []
#     # for time in hypnogram_info.values():
#     #     time_stages.append(time)

#     # print("The TIME STAGES for JSON is:", time_stages)

#     # =========================================================
#     time_stages = datetime_functions.create_time_stages(
#         hypnogram_time_dict, total_sleep_hrs
#     )

#     print("THE TIME STAGE ON SERVER.PY side is:", time_stages)

#     time_lst = datetime_functions.create_total_time_lst(time_stages)

#     print("The TIME LST on SERVER.PY side is", time_lst)

#     final_time_dict = datetime_functions.create_time_final_dict(
#         time_stages, time_lst, total_sleep_hrs
#     )
#     print("DOES FINAL time dict work?:", final_time_dict)
#     # =========================================================
#     # hypnogram_data = []

#     # for time_stage, sleep_stage in final_time_dict.items():

#     #     hypnogram_data.append(
#     #         {"sleep_mins": time_stage, "sleep_stages": sleep_stage,}
#     #     )

#     # print("The data going INTO Chart.js Hypnogram is:", hypnogram_data)

#     # CHART.JS Hypnogram==================
#     sleep_labels = []
#     time_data = []
#     for key_time, value_stage in final_time_dict.items():
#         time_data.append(key_time)
#         sleep_labels.append(value_stage)

#     # // TODO: There is a bug where the time added is wrong. Example, 9.19 hrs for Nov 16th is about 551.4min, however, it returns over 630min. No problem with function in Sublime
#     print()
#     print("THE LABELS for Hynogram is:", sleep_labels)
#     print("THE DATA for hynoogram is:", time_data)
#     print()
#     # return jsonify(labels, data)  #Returning object

#     # CHART.JS Doughnut======================

#     doughnut_data_dict = datetime_functions.create_doughnut_chart(
#         hypnogram_time_dict, total_sleep_min
#     )

#     print()
#     print("THE Data from the DOUGHNUT dict is:", doughnut_data_dict)
#     print()

#     doughnut_percent_lst = []
#     doughnut_name_lst = []

#     for sleep_name, percentage in doughnut_data_dict.items():
#         doughnut_name_lst.append(sleep_name)
#         doughnut_percent_lst.append(f"{percentage:.2f}")

#     print("The DOUGHNUT percents is:", doughnut_percent_lst)
#     print("The DOUGHNUT Name is:", doughnut_name_lst)

#     # doughnut_data_lst = []
#     # awake_percentage = doughnut_data_dict.get("Awake")
#     # awake_percentage_formatted = "{:.2f}".format(awake_percentage)
#     # print("The AWAKE PERCENTAGE IS:", awake_percentage_formatted)

#     # light_sleep_percentage = doughnut_data_dict.get("Light Sleep")
#     # light_sleep_percentage_formatted = "{:.2f}".format(light_sleep_percentage)

#     # deep_sleep_percentage = doughnut_data_dict.get("Deep Sleep")
#     # deep_sleep_percentage_formatted = "{:.2f}".format(deep_sleep_percentage)

#     # rem_sleep_percentage = doughnut_data_dict.get("REM Sleep")
#     # rem_sleep_percentage_formatted = "{:.2f}".format(rem_sleep_percentage)

#     hynogram_doughnut_data = {
#         "sleep_labels": sleep_labels,
#         "time_data": time_data,
#         "doughnut_name": doughnut_name_lst,
#         "doughnut_percent": doughnut_percent_lst,
#     }
#     return jsonify({"data": hynogram_doughnut_data})

#     # return jsonify({"data": hypnogram_data})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
