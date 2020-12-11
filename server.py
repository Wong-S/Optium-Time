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


app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = True

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
API_KEY = os.environ["YOUTUBE_KEY"]

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# ================================================================================
@app.route("/")
def create_homepage():
    """Return homepage"""

    return render_template("homepage.html")


# ================================================================================
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
    check_email = crud.get_user_by_email(email)

    if check_email == None:
        crud.create_user(first_name, last_name, email, password, timezone)
        flash("New account created successfully! Please log in")

    else:
        flash("Email is associated with an account. Try again!")

    return redirect("/")


@app.route("/login")
def check_login_credentials():
    """Return journal webpage or redirect to homepage"""

    email = request.args.get("login_email")
    password = request.args.get("login_password")

    match_passwords = crud.check_password(email, password)

    user_details = crud.get_user_by_email(email)

    if match_passwords == True:
        session["user"] = user_details.user_id
        session["user_name"] = user_details.first_name

        session["timezone"] = user_details.timezone
        return redirect("/user-page")
    else:
        flash("Email or password do not match. Try again!")
        return redirect("/")


# =====================================================================
@app.route("/user-page", methods=["GET", "POST"])
def display_user_options():
    """Return user's next selection"""

    user_id = session["user"]

    user_obj = crud.get_user_by_id(user_id)

    user_timezone = session["timezone"]

    chosen_month_by_user_str = datetime_functions.current_date_timezone_from_utc_with_month_format(
        user_timezone
    )

    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    all_date_obj_lst = []
    for data in sleep_log_user_obj.sleep_logs:

        all_date_obj_lst.append(data.current_date)

    all_datetime_str_lst = datetime_functions.create_date_str(all_date_obj_lst)

    converted_dates_obj_to_str = datetime_functions.convert_date_obj_to_str_format(
        all_date_obj_lst
    )

    all_month_dict = {
        converted_dates_obj_to_str[i]: all_datetime_str_lst[i]
        for i in range(len(converted_dates_obj_to_str))
    }

    selected_month_filter_str_lst = []

    for k, v in all_month_dict.items():
        if v == chosen_month_by_user_str:

            selected_month_filter_str_lst.append(k)

    month_date_obj_lst = datetime_functions.create_filtered_date_obj_from_str_lst(
        selected_month_filter_str_lst
    )

    user_sleep_log_obj_for_date_lst = crud.get_sleep_time_by_filtered_month_lst(
        user_id, month_date_obj_lst
    )

    timezone = session["timezone"]

    total_time_hours_lst = []
    for i in user_sleep_log_obj_for_date_lst:
        total_subtracted_hours = datetime_functions.time_difference(
            timezone, i.wake_time, i.bed_time
        )
        total_time_hours_lst.append(total_subtracted_hours)

    month_date_converted_to_str = datetime_functions.create_date_str_with_different_format(
        month_date_obj_lst
    )

    session["month_total_hours"] = total_time_hours_lst
    session["month_dates"] = month_date_converted_to_str

    if "set-alarm-wake-time" in session:
        alarm_wake_time = session["set-alarm-wake-time"]

        new_time_str = datetime_functions.format_time_str(alarm_wake_time)

        return render_template(
            "user_page.html",
            user_obj=user_obj,
            new_time_str=f"Alarm Set: {new_time_str}",
            user_id=user_id,
        )
    else:

        new_time_str = "No Alarm Set"
        return render_template(
            "user_page.html",
            user_obj=user_obj,
            new_time_str=new_time_str,
            user_id=user_id,
        )


# =====================================================================
@app.route("/journal/<user_id>")
def journal_entry(user_id):
    """Return journal page """

    return render_template("journal_creation.html", user_id=user_id)


@app.route("/journal-current-entries/<user_id>")
def display_journal_information(user_id):
    """Show all user's journal information"""

    user_obj = crud.check_user_to_journal_id(user_id)

    return render_template("journal_details.html", user_obj=user_obj)


@app.route("/journal-new-entries/<user_id>")
def display_new_journal(user_id):
    """Return new journal page"""

    return render_template("journal_creation.html", user_id=user_id)


@app.route("/journals/<user_id>", methods=["POST"])
def register_journal_entry(user_id):
    """Create a new journal entry per user"""

    entry_name = request.form.get("entry-name")
    entry_details = request.form.get("entry-details")

    timezone = session["timezone"]
    created_at = datetime_functions.current_date_timezone_from_utc(timezone)
    updated_at = datetime_functions.current_date_timezone_from_utc(timezone)

    crud.create_journal_entry(
        user_id, entry_name, entry_details, created_at, updated_at
    )
    flash("New entry made!!")

    return render_template("journal_creation.html", user_id=user_id)


# =====================================================================
@app.route("/video-playlist/<user_id>")
def playlist_video_page(user_id):
    """Return playlist and video options """

    return render_template("playlist-video.html", user_id=user_id)


@app.route("/video-categories/<user_id>")
def video_category_list(user_id):
    """Return list of video category selections"""

    return render_template("video-categories.html", user_id=user_id)


@app.route("/video-selection/<user_id>")
def display_video_selection(user_id):
    """Query selected video filter and display to frontend"""

    video_category = request.args.getlist("categories")

    video_duration = request.args.get("duration")

    display_videos = crud.display_selected_videos(video_category, video_duration)

    session["videos"] = (
        display_videos,
        video_category,
        video_duration,
    )

    return render_template(
        "video-displays.html", user_id=user_id, display_videos=display_videos
    )


@app.route("/register-videos/<user_id>", methods=["POST"])
def register_videos(user_id):
    """Store video and playlist in video database"""

    user_obj = crud.check_user_to_playlist_id(user_id)

    playlist_name = request.form.get("playlist-name")

    playlist_obj = crud.create_playlist(playlist_name, user_id)
    playlist_id = playlist_obj.playlist_id

    video_list = request.form.getlist("video-list")

    n = 1
    video_url_id = [video[n] for video in session["videos"][0]]

    n = 0
    video_title = [video[n] for video in session["videos"][0]]

    video_duration = session["videos"][2]

    video_category_name = session["videos"][1]

    dict_video = {video_url_id[i]: video_title[i] for i in range(len(video_url_id))}

    for video_ids in video_list:

        if video_ids in video_url_id:
            video_title = dict_video[video_ids]
            crud.create_video(video_title, video_duration, video_ids, playlist_id)

    return render_template(
        "current_playlists.html",
        user_id=user_id,
        video_list=video_list,
        playlist_obj=playlist_obj,
        user_obj=user_obj,
    )


@app.route("/current-playlist/<user_id>")
def view_playlist(user_id):
    """Return videos stored in playlist"""

    user_obj = crud.check_user_to_playlist_id(user_id)

    return render_template("current_playlists.html", user_obj=user_obj, user_id=user_id)


@app.route("/display-playlist-videos/<playlist_id>")
def display_videos_in_playlist(playlist_id):
    """Return videos in selected playlist"""

    user_id = session["user"]

    playlist_video_obj = crud.get_videos_from_playlist_id(playlist_id)

    return render_template(
        "display_playlist_videos.html",
        playlist_video_obj=playlist_video_obj,
        user_id=user_id,
    )


# =====================================================================
@app.route("/set-alarm/<user_id>")
def display_alarm_clock(user_id):
    """Return alarm clock options"""

    return render_template("set_alarm.html", user_id=user_id)


@app.route("/set-alarm/<user_id>", methods=["POST"])
def register_alarm(user_id):
    """Store wake up and bed time to database"""

    wake_time = request.form.get("alarm-wake")

    wake_add_sec_time = ":00"
    wake_time = wake_time + wake_add_sec_time

    session["set-alarm-wake-time"] = wake_time

    user_timezone = session["timezone"]

    bed_time = datetime_functions.current_time_timezone_from_utc(user_timezone)

    current_date = datetime_functions.current_date_timezone_from_utc(user_timezone)

    session["current_date"] = current_date

    crud.create_sleep_log(user_id, wake_time, bed_time, current_date)

    user_total_time = datetime_functions.time_difference(
        user_timezone, wake_time, bed_time
    )

    session["alarm"] = user_total_time

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

    alarm_dict = {"hours": alarm_hours, "minutes": alarm_minutes}

    return alarm_dict


# =================================================
@app.route("/countdown-timer-message-twilio")
def display_countdown_timer():
    """Return countdown timer page of set alarm"""

    alarm_num_time = session["alarm"]
    user_first_name = session["user_name"]
    twilio_message = datetime_functions.countdown_message(
        alarm_num_time, user_first_name
    )

    return jsonify(twilio_message)


# =================================================
@app.route("/sleep-log")
def display_sleep_graph_options():
    """Return sleep graphs page"""

    user_id = session["user"]

    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    converted_current_date = []
    for date in sleep_log_user_obj.sleep_logs:
        current_date = date.current_date
        converted_current_date.append(current_date.strftime("%b-%d-%Y"))

    converted_current_date_for_grouping_obj = []

    for date in sleep_log_user_obj.sleep_logs:
        current_date = date.current_date
        converted_current_date_for_grouping_obj.append(current_date)

    session["dates_group_obj"] = converted_current_date

    dates_grouped_by_seven = []
    for x in range(0, len(converted_current_date_for_grouping_obj), 7):
        dates_grouped_by_seven.append(
            converted_current_date_for_grouping_obj[x : x + 7]
        )

    return render_template(
        "sleep_graphs.html",
        user_id=user_id,
        sleep_log_user_obj=sleep_log_user_obj,
        converted_current_date=converted_current_date,
        dates_grouped_by_seven=dates_grouped_by_seven,
    )


@app.route("/month-date-only", methods=["GET", "POST"])
def display_date_info_chosen_from_month_graph():
    """Return specific date and journal info"""

    if request.method == "POST":

        user_id = session["user"]

        data = request.get_json()

        date = data["information"]["date"]

        if "post_date" in session:

            session.pop("post_date")

            session["post_date"] = date
        else:

            session["post_date"] = date

        datee = session.get("post_date")

        return redirect("/month-date-only")

    if request.method == "GET":

        chosen_date_str = session.get("post_date")

        user_id = session["user"]

        chosen_date_by_user_obj = datetime_functions.change_filtered_dates_different_format_to_obj(
            chosen_date_str
        )

        filtered_date_obj = crud.get_sleep_data_by_filtered_date(
            user_id, chosen_date_by_user_obj
        )

        filtered_date_wake_time_obj = filtered_date_obj.wake_time

        wake_time_str = str(filtered_date_wake_time_obj)
        wake_time_new_str = datetime_functions.format_time_str(wake_time_str)

        if wake_time_new_str[-2:] == "PM":
            wake_time_num_slice = int(wake_time_str[0:2]) - 12

            new_wake_time_str = (
                str(wake_time_num_slice) + wake_time_str[2:5] + " " + "PM"
            )
            wake_time_new_str = new_wake_time_str

        elif wake_time_new_str[-2:] == "AM":
            wake_time_new_str = wake_time_new_str[1:]

        filtered_date_bed_time_obj = filtered_date_obj.bed_time

        bed_time_str = str(filtered_date_bed_time_obj)

        bed_time_new_str = datetime_functions.format_time_str(bed_time_str)

        if bed_time_new_str[-2:] == "PM":
            bed_time_num_slice = int(bed_time_str[0:2]) - 12

            new_bed_time_str = str(bed_time_num_slice) + bed_time_str[2:5] + " " + "PM"
            bed_time_new_str = new_bed_time_str

        elif bed_time_new_str[-2:] == "AM":
            bed_time_new_str = bed_time_new_str[1:]

        user_obj = crud.check_user_to_journal_id(user_id)

        journal_titles_by_date = {}
        for date in user_obj.journals:
            if chosen_date_by_user_obj == date.created_at:

                journal_titles_by_date[date.entry_name] = date.entry_details

        # ===================================================================
        user_timezone = session["timezone"]

        total_sleep_hours_this_day = datetime_functions.time_difference(
            user_timezone, filtered_date_wake_time_obj, filtered_date_bed_time_obj
        )

        session["total_sleep_hours"] = total_sleep_hours_this_day
        total_sleep_hrs = session["total_sleep_hours"]

        hypnogram_dict = datetime_functions.create_hypnogram(total_sleep_hours_this_day)

        session["hypnogram"] = hypnogram_dict

        hypnogram_info = session["hypnogram"]

        return render_template(
            "month_date_chosen.html",
            chosen_date=chosen_date_str,
            user_id=user_id,
            wake_time=wake_time_new_str,
            bed_time=bed_time_new_str,
            journal_titles_by_date=journal_titles_by_date,
        )


@app.route("/date-filter/<user_id>")
def display_chosen_sleep_date(user_id):
    """Return date information of via filter"""

    chosen_date_by_user_str = request.args.get("date-start")

    chosen_date_by_user_obj = datetime_functions.create_filtered_date_obj(
        chosen_date_by_user_str
    )

    filtered_date_obj = crud.get_sleep_data_by_filtered_date(
        user_id, chosen_date_by_user_obj
    )

    if filtered_date_obj is None:
        flash("The date you selected does not exist")
        return redirect("/sleep-log")

    else:
        filtered_date = filtered_date_obj.current_date

        grouped_per_week = session["dates_group_obj"]

        grouped_per_week_obj = []
        for i in grouped_per_week:
            grouped_per_week_obj.append(
                datetime_functions.change_filtered_dates_to_obj(i)
            )

        dates_grouped_by_seven = []
        for x in range(0, len(grouped_per_week_obj), 7):
            dates_grouped_by_seven.append(grouped_per_week_obj[x : x + 7])

        selected_group_dates_obj_lst = []
        for date in dates_grouped_by_seven:
            if filtered_date in date:
                selected_group_dates_obj_lst.append(date)

        converted_current_date_str = []
        for date_lst in selected_group_dates_obj_lst:
            for date in date_lst:
                converted_current_date_str.append(date.strftime("%b-%d-%Y"))

        session["final_weekly_dates"] = converted_current_date_str

        pre_time_sleep_log_obj = crud.get_sleep_time_by_filtered_date_lst(
            user_id, selected_group_dates_obj_lst
        )

        timezone = session["timezone"]

        total_time_hours_lst = []
        for i in pre_time_sleep_log_obj:
            total_subtracted_hours = datetime_functions.time_difference(
                timezone, i.wake_time, i.bed_time
            )
            total_time_hours_lst.append(total_subtracted_hours)

        session["total_weekly_hrs_json"] = total_time_hours_lst

        weekly_hours_lst = session["total_weekly_hrs_json"]

        average_hrs = datetime_functions.calculate_weekly_avg_hrs(weekly_hours_lst)

        return render_template(
            "sleep_dates_by_week.html",
            filtered_date=filtered_date,
            average_hrs=average_hrs,
            user_id=user_id,
        )


@app.route("/weekly-sleep-data.json")
def weekly_dates_json():
    """Return JSON dict to chart.js"""

    weekly_date_lst_obj = session["final_weekly_dates"]

    total_hrs = session["total_weekly_hrs_json"]

    weekly_sleep_data = {
        "total_hours": total_hrs,
        "dates_over_time": weekly_date_lst_obj,
    }

    return jsonify({"data": weekly_sleep_data})


# =======================
@app.route("/month-filter/<user_id>")
def filter_by_month(user_id):
    """Return dates by month"""

    chosen_month_by_user_str = request.args.get("start-month")

    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    all_date_obj_lst = []
    for data in sleep_log_user_obj.sleep_logs:

        all_date_obj_lst.append(data.current_date)

    all_datetime_str_lst = datetime_functions.create_date_str(all_date_obj_lst)

    converted_dates_obj_to_str = datetime_functions.convert_date_obj_to_str_format(
        all_date_obj_lst
    )

    all_month_dict = {
        converted_dates_obj_to_str[i]: all_datetime_str_lst[i]
        for i in range(len(converted_dates_obj_to_str))
    }

    selected_month_filter_str_lst = []

    for k, v in all_month_dict.items():
        if v == chosen_month_by_user_str:
            selected_month_filter_str_lst.append(k)

    month_date_obj_lst = datetime_functions.create_filtered_date_obj_from_str_lst(
        selected_month_filter_str_lst
    )

    user_sleep_log_obj_for_date_lst = crud.get_sleep_time_by_filtered_month_lst(
        user_id, month_date_obj_lst
    )

    timezone = session["timezone"]

    total_time_hours_lst = []
    for i in user_sleep_log_obj_for_date_lst:
        total_subtracted_hours = datetime_functions.time_difference(
            timezone, i.wake_time, i.bed_time
        )
        total_time_hours_lst.append(total_subtracted_hours)

    month_date_converted_to_str = datetime_functions.create_date_str_with_different_format(
        month_date_obj_lst
    )

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

    all_dates_in_month = session["month_dates"]

    monthly_sleep_data = {
        "total_monthly_hours": total_monthly_hours,
        "monthly_dates_over_time": all_dates_in_month,
    }

    return jsonify({"data": monthly_sleep_data})


@app.route("/sleep-data-by-date/<user_id>/<date>")
def display_sleep_times_for_date(user_id, date):
    """Return sleep wake and bed time page"""

    date_obj = datetime_functions.create_date_obj(date)

    user_id = session["user"]
    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    current_date_lst = []
    for date in sleep_log_user_obj.sleep_logs:

        current_date_lst.append(date.current_date)

    wake_bed_times_obj = crud.get_sleep_data_by_date(
        user_id, current_date_lst, date_obj
    )

    unconverted_current_date = wake_bed_times_obj.current_date

    session["datetime_object_current_date"] = unconverted_current_date

    converted_current_date = unconverted_current_date.strftime("%b-%d-%Y")

    # ==============================

    user_obj = crud.check_user_to_journal_id(user_id)

    journal_titles_by_date = {}
    for date in user_obj.journals:
        if unconverted_current_date == date.created_at:
            journal_titles_by_date[date.entry_name] = date.entry_details

    return render_template(
        "sleep_bed_wake_times.html",
        user_id=user_id,
        converted_current_date=converted_current_date,
        sleep_log_user_obj=sleep_log_user_obj,
        wake_bed_times_obj=wake_bed_times_obj,
        journal_titles_by_date=journal_titles_by_date,
    )


# ===================================================
@app.route("/journal-entries/<entry_details>")
def read_journals(entry_details):

    return render_template("choosen_journal_details.html", entry_details=entry_details)


# ===================================================
@app.route("/total-sleep.json")
def get_total_sleep():
    """Get total sleep per day"""

    user_id = session["user"]

    sleep_log_user_obj = crud.get_sleep_data_user_id(user_id)

    sleep_hours_this_day = []
    for date in sleep_log_user_obj.sleep_logs:

        current_date = date.current_date
        converted_current_date_this_day = current_date.strftime("%b-%d-%Y")

        user_timezone = session["timezone"]

        total_sleep_hours_this_day = datetime_functions.time_difference(
            user_timezone, date.wake_time, date.bed_time
        )

        sleep_hours_this_day.append(
            {
                "date": converted_current_date_this_day,
                "sleep_hours": total_sleep_hours_this_day,
            }
        )

    return jsonify({"data": sleep_hours_this_day})


@app.route("/hypnogram-sleep.json")
def get_individual_sleep_times():
    """Get total sleep per day and Return JSON dictionary for Chart.js"""

    total_sleep_hrs = session["total_sleep_hours"]

    total_sleep_min = total_sleep_hrs * 60

    hypnogram_time_dict = session["hypnogram"]

    time_stages = datetime_functions.create_time_stages(
        hypnogram_time_dict, total_sleep_hrs
    )

    time_lst = datetime_functions.create_total_time_lst(time_stages)

    final_time_dict = datetime_functions.create_time_final_dict(
        time_stages, time_lst, total_sleep_hrs
    )

    sleep_labels = [0]
    time_data = [0]
    for key_time, value_stage in final_time_dict.items():
        time_data.append(key_time)
        sleep_labels.append(value_stage)

    doughnut_data_dict = datetime_functions.create_doughnut_chart(
        hypnogram_time_dict, total_sleep_min
    )

    doughnut_percent_lst = []
    doughnut_name_lst = []

    for sleep_name, percentage in doughnut_data_dict.items():
        doughnut_name_lst.append(sleep_name)
        doughnut_percent_lst.append(f"{percentage:.2f}")

    hynogram_doughnut_data = {
        "sleep_labels": sleep_labels,
        "time_data": time_data,
        "doughnut_name": doughnut_name_lst,
        "doughnut_percent": doughnut_percent_lst,
    }
    return jsonify({"data": hynogram_doughnut_data})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
