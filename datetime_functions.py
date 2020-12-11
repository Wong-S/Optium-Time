from random import random, randint, choice

from datetime import datetime

import time

import pytz


import os
from twilio.rest import Client


UTC = pytz.utc


central_time = pytz.timezone("US/Central")
eastern_time = pytz.timezone("US/Eastern")
pacific_time = pytz.timezone("US/Pacific")
mountain_time = pytz.timezone("US/Mountain")
alaska_time = pytz.timezone("US/Alaska")
hawaii_time = pytz.timezone("US/Hawaii")


def current_time_timezone_from_utc(timezone):
    """Return Time in UTC active timezone"""

    user_timezone = pytz.timezone(timezone)
    utc_datetime = datetime.now(user_timezone)

    return utc_datetime.strftime("%H:%M:%S")


def current_date_timezone_from_utc(timezone):
    """Return Date in UTC active timezone"""

    user_timezone = pytz.timezone(timezone)
    utc_datetime = datetime.now(user_timezone).date()

    return utc_datetime


def current_date_timezone_from_utc_with_month_format(timezone):
    """Return month in UTC active timezone"""

    user_timezone = pytz.timezone(timezone)
    utc_month_datetime = datetime.now(user_timezone).date()
    utc_month_datetime = utc_month_datetime.strftime("%Y-%m")

    return utc_month_datetime


# ==================================================
def format_time_str(time_str):
    """Return a newly formatted time string"""

    time_obj = datetime.strptime(time_str, "%H:%M:%S")

    new_time_str = datetime.strftime(time_obj, "%H:%M %p")

    return new_time_str


# ==================================================
def create_date_obj(date_str):
    """Return a datetime.date object"""

    datetime_obj = datetime.strptime(date_str, "%b-%d-%Y")

    return datetime.date(datetime_obj)


def create_filtered_date_obj(date_str):
    """Return a datetime.date object"""

    datetime_obj = datetime.strptime(date_str, "%Y-%m-%d")

    return datetime.date(datetime_obj)


def create_filtered_date_obj_from_str_lst(date_str_lst):
    """Return a datetime.date object from date str lst"""

    month_datetime_datetime_obj_lst = []

    for date_str in date_str_lst:
        month_date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        month_datetime_datetime_obj_lst.append(month_date_obj)

    month_datetime_date_obj_lst = []
    for date in month_datetime_datetime_obj_lst:

        month_datetime_date_obj_lst.append(datetime.date(date))

    return month_datetime_date_obj_lst


def change_filtered_dates_to_obj(date_str):
    """Return a datetime.date object"""

    datetime_obj = datetime.strptime(date_str, "%b-%d-%Y")

    return datetime.date(datetime_obj)


# FIXME !!!!!  11/30
def change_filtered_dates_different_format_to_obj(date_str):
    """Return a datetime.date object"""

    datetime_obj = datetime.strptime(date_str, "%m/%d/%Y")

    return datetime.date(datetime_obj)


def calculate_weekly_avg_hrs(total_hours_lst):
    """Return average hours slept per week"""

    sum = 0
    for hour in total_hours_lst:
        sum += hour

    average_hrs = sum / 7

    return f"{average_hrs:.2f}"


# ======================================
def create_date_str(date_obj_lst):
    """Return datetime.date string from datetime.date obj"""

    all_datetime_str_lst = []
    for date_obj in date_obj_lst:
        datetime_str = datetime.strftime(date_obj, "%Y-%m")

        all_datetime_str_lst.append(datetime_str)

    return all_datetime_str_lst


def convert_date_obj_to_str_format(date_obj_lst):
    """Return lst of datetime.date strings"""

    converted_dates_obj_to_str = []

    for date_obj in date_obj_lst:
        datetime_str = datetime.strftime(date_obj, "%Y-%m-%d")

        converted_dates_obj_to_str.append(datetime_str)

    return converted_dates_obj_to_str


def create_date_str_with_different_format(date_obj_lst):
    """Return datetime.date string from datetime.date obj"""

    all_datetime_str_lst = []
    for date_obj in date_obj_lst:
        datetime_str = datetime.strftime(date_obj, "%m/%d/%Y")

        all_datetime_str_lst.append(datetime_str)

    return all_datetime_str_lst


# ==================================================
def time_difference(timezone, wake_time, bed_time):
    """Return total time difference"""

    format = "%H:%M:%S"

    date_timez = current_date_timezone_from_utc(timezone)

    wake_time = str(wake_time)

    bed_time = str(bed_time)

    wake_time = datetime.strptime(wake_time, "%H:%M:%S")

    wake_time_obj = datetime.time(wake_time)

    bed_time = datetime.strptime(bed_time, "%H:%M:%S")

    bed_time_obj = datetime.time(bed_time)

    date_time_wake = datetime.combine(date_timez, wake_time_obj)

    time_wake_obj = datetime.time(date_time_wake)

    date_time_bed = datetime.combine(date_timez, bed_time_obj)

    time_bed_obj = datetime.time(date_time_bed)

    timeStr_wake = time_wake_obj.strftime("%H:%M:%S")

    timeStr_bed = time_bed_obj.strftime("%H:%M:%S")

    date_time_difference = datetime.strptime(timeStr_wake, format) - datetime.strptime(
        timeStr_bed, format
    )

    days, seconds = date_time_difference.days, date_time_difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_diff = f"{hours}.{minutes}"
    time_diff = float(time_diff)

    return time_diff


# ===============================================
def create_hypnogram(total_sleep_hours):
    """Return dictionary with 4 sleep stages"""

    total_sleep_min = total_sleep_hours * 60

    sleep_cycle = total_sleep_min // 90

    time_dict = {}

    i = 0
    while i < sleep_cycle:

        if i < 1:
            awake_stage = randint(12, 15)

            time_dict["awake"] = [awake_stage]

            time_dict["REM"] = [10]

            stage_1 = randint(5, 10)

            time_dict["NREM1"] = stage_1

            stage_2 = randint(10, 25)

            time_dict["NREM2"] = [stage_2]

            total_sleep_before_rem = awake_stage + stage_1 + stage_2 + 10

            time_difference_before_rem_stage = 90 - total_sleep_before_rem

            time_dict["NREM3"] = [time_difference_before_rem_stage]

            i += 1

        elif i < (sleep_cycle - 1):

            stage_2 = randint(30, 60)

            time_dict["NREM2"].append(stage_2)

            stage_3_4 = randint(10, 20)

            time_dict["NREM3"].append(stage_3_4)

            total_sleep_before_rem = stage_2 + stage_3_4

            time_difference_before_rem_stage = 90 - total_sleep_before_rem

            time_dict["REM"].append(time_difference_before_rem_stage)

            i += 1

        else:

            awake_stage = randint(12, 15)

            time_dict["awake"].append(awake_stage)

            stage_2 = randint(20, 40)

            time_dict["NREM2"].append(stage_2)

            stage_3_4 = randint(10, 20)

            time_dict["NREM3"].append(stage_3_4)

            total_sleep_before_rem = awake_stage + stage_2 + stage_3_4

            time_difference_before_rem_stage = 90 - total_sleep_before_rem

            time_dict["REM"].append(time_difference_before_rem_stage)

            i += 1

    return time_dict


def create_time_stages(time_dict, total_sleep_hours):
    """Return dictionary with sleep stages with sleep time"""

    total_sleep_min = total_sleep_hours * 60

    # Sleep cycles last about 90 min?
    sleep_cycle = total_sleep_min // 90

    time_stages = []

    i = 0
    while i < sleep_cycle:
        if i < 1:
            awake = time_dict.get("awake")
            time_stages.append(awake[0])
            awake.pop(0)

            stage_1 = time_dict.get("NREM1")
            time_stages.append(stage_1)

            stage_2 = time_dict.get("NREM2")
            time_stages.append(stage_2[0])

            stage_3 = time_dict.get("NREM3")
            time_stages.append(stage_3[0])

            rem = time_dict.get("REM")
            time_stages.append(rem[0])

            i += 1

        elif i < sleep_cycle - 1:

            time_stages.append(stage_2[i])

            time_stages.append(stage_3[i])

            time_stages.append(rem[i])

            i += 1

        else:

            time_stages.append(stage_2[i])
            time_stages.append(stage_3[i])
            time_stages.append(rem[i])
            time_stages.append(awake[0])

            break

    return time_stages


# ======================================================================================
def create_total_time_lst(time_stages):
    """Return a list with times adding to total minutes of sleep cycle"""

    time_lst = []

    num = time_stages[0]
    time_lst.append(num)

    for i in range(len(time_stages) - 1):

        next_num = time_stages[i + 1]

        num += next_num

        time_lst.append(num)

        i += 1

    return time_lst


# ======================================================================================
def create_time_final_dict(time_stages, time_lst, total_sleep_hrs):
    """"Return dictionary with time stage and time minutes to JSON"""

    final_time_dict = {}

    total_sleep_min = total_sleep_hrs * 60

    sleep_cycle = total_sleep_min // 90

    first_sleep_stage_lst = [5, 3, 2, 1, 4]
    middle_sleep_stage_lst = [2, 1, 4]

    last_sleep_stage_lst = [2, 1, 4, 5]
    i = 0
    while i < sleep_cycle:

        if i < 1:
            time_lst_first_slice = time_lst[0:5]

            for time_key in time_lst_first_slice:
                for stage_value in first_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    first_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

        elif i < sleep_cycle - 1:

            middle_length = len(middle_sleep_stage_lst)

            time_slice_middle = time_lst[5:]

            slice_length = len(time_slice_middle) - 4

            new_middle_lst = []

            while middle_length < slice_length:
                for sleep_stage in middle_sleep_stage_lst:
                    new_middle_lst.append(sleep_stage)

                    middle_length += 1

            final_middle_sleep_stage_lst = middle_sleep_stage_lst + new_middle_lst

            for time_key in time_slice_middle:
                for stage_value in final_middle_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    final_middle_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

        else:

            time_lst_last_slice = time_lst[-4:]

            for time_key in time_lst_last_slice:
                for stage_value in last_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    last_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

    return final_time_dict


# ===============================================
def calculate_sleep_stage_percent(sleep_stage, total_sleep_time):
    """Return the percent of each sleep stage"""

    sum = 0
    for i in sleep_stage:
        sum += i

        sleep_percentile = (sum / total_sleep_time) * 100

    return sleep_percentile


def create_doughnut_chart(time_dict, total_sleep_time):
    """Return percentile of each sleep stage as a dictionary"""

    doughnut_dict = {}

    awake = time_dict.get("awake")

    awake_percent = calculate_sleep_stage_percent(awake, total_sleep_time)

    doughnut_dict["Awake"] = awake_percent

    stage_1 = time_dict.get("NREM1")
    stage_1_percent = (stage_1 / total_sleep_time) * 100

    stage_2 = time_dict.get("NREM2")

    stage_2_percent = calculate_sleep_stage_percent(stage_2, total_sleep_time)

    doughnut_dict["Light Sleep"] = stage_1_percent + stage_2_percent

    stage_3 = time_dict.get("NREM3")

    stage_3_percent = calculate_sleep_stage_percent(stage_3, total_sleep_time)

    doughnut_dict["Deep Sleep"] = stage_3_percent

    rem = time_dict.get("REM")
    rem_percent = calculate_sleep_stage_percent(rem, total_sleep_time)

    doughnut_dict["REM Sleep"] = rem_percent

    return doughnut_dict


# ==================================
def countdown_message(num_time, user_name):

    str_time = str(num_time)
    time_lst = str_time.split(".")

    hours = int(time_lst[0])
    minutes = int(time_lst[1])

    total_seconds = (hours * 3600) + (minutes * 60)

    total_min = total_seconds / 60
    total_sleep_cycles = total_min // 90

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f" Hello {user_name}! You slept for a total of 6 hours and 11 minutes. The total number of sleep cycles from this sleep period was 4. You can always view your full sleep log report and NREM/REM time in your profile.",
        from_="+12028049589",
        to="+12817145109",
    )

    return message.sid

