from random import random, randint, choice

from datetime import datetime


# from dateutil.parser import *
import pytz

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location

# IST = pytz.timezone("Asia/Kolkata")
# timeZ_Ny = pytz.timezone("America/New_York")
# timeZ_Ma = pytz.timezone("Africa/Maseru")
# timeZ_At = pytz.timezone("Europe/Athens")

# The 6 timezones listed below!!! For USA only for now...
central_time = pytz.timezone("US/Central")
eastern_time = pytz.timezone("US/Eastern")
pacific_time = pytz.timezone("US/Pacific")
mountain_time = pytz.timezone("US/Mountain")
alaska_time = pytz.timezone("US/Alaska")
hawaii_time = pytz.timezone("US/Hawaii")

# print the date and time in
# standard format
# print("UTC in Default Format : ", datetime.now(UTC))

# India Standard Time:
# print("IST in Default Format : ", datetime.now(IST))

# print the date and time in
# specified format
# datetime_utc_1 = datetime.now(central_time)
# print(datetime_utc_1)
# datetime_utc_1 = datetime_utc_1.strftime("%H %M %S")

# datetime_utc_2 = datetime.now(eastern_time)
# datetime_utc_2 = datetime_utc_2.strftime("%H %M %S")

# datetime_utc_2 = int(datetime_utc_2)
# print(type(datetime_utc_2))

# datetime_utc_3 = int(datetime_utc_2) - int(datetime_utc_1)
# print(datetime_utc_3)


# datetime_ist = datetime.now(IST)
# print("Date & Time in IST : ", datetime_ist.strftime("%Y:%m:%d %H:%M:%S %Z %z"))


def current_time_timezone_from_utc(timezone):
    """Return Time in UTC active timezone"""

    user_timezone = pytz.timezone(timezone)
    utc_datetime = datetime.now(user_timezone)  # FIXME: This returns the date of TODAY!
    print("Date & Time in UTC : ", utc_datetime.strftime("%H:%M"))

    return utc_datetime.strftime("%H:%M")  # Returning a STRING


def current_date_timezone_from_utc(timezone):
    """Return Date in UTC active timezone"""

    user_timezone = pytz.timezone(timezone)
    utc_datetime = datetime.now(user_timezone).date()
    print("Date & Time in UTC : ", utc_datetime.strftime("%m-%d-%Y"))

    return utc_datetime  # This is returning a datetime object
    # return utc_datetime.strftime("%m-%d-%Y")


# ==================================================
def create_date_obj(date_str):
    """Return a datetime.date object"""

    print("If you made it here, the argument passed is:", date_str)

    datetime_obj = datetime.strptime(
        date_str, "%b-%d-%Y"
    )  # NOTE: The date_str passed in is the converted one. So Nov-25-2020. And this must match the format!

    return datetime.date(datetime_obj)


# ==================================================
# NOTE: For example when subtracting time:
# x = timezone_from_utc("US/Central")
# y = timezone_from_utc("US/Pacific")


# format = "%H:%M"
# time = datetime.strptime(x, format) - datetime.strptime(y, format)
# print(time)

# time_difference("US/Central", "07:30:00", "23:30:00")
def time_difference(timezone, wake_time, bed_time):
    """Return total time difference"""

    format = "%H:%M:%S"
    # total_time = datetime.strptime(wake_time, format) - datetime.strptime(
    #     bed_time, format
    # )
    date_timez = current_date_timezone_from_utc(timezone)

    # NOTE: To calculate the difference, you have to convert the datetime.time object to a datetime.datetime object. Then when you subtract, you get a timedelta object. In order to find out how many hours the timedelta object is, you have to find the total seconds and divide it by 3600.

    ######################### These two functions were made to compensate for the string formatted times passed into the database from my original file
    # wake_time = parser.parse(wake_time)
    # bed_time = parser.parse(bed_time)
    # wake_time = datetime.time(wake_time)
    # bed_time = datetime.time(bed_time)
    # wake_time_obj = datetime.strptime(date_timez wake_time, format)
    # bed_time_obj = datetime.strptime(date_timez bed_time, format)

    # datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    # print(bed_time)
    #########################

    # time_1 = "07:30:00"
    # time_1_obj = datetime.strptime(time_1, '%H:%M:%S')
    # print(time_1_obj)

    # time_2 = datetime.time(time_1_obj)
    # print(time_2)
    print(type(wake_time))  # THESE ARE BOTH DATETIME Objects
    print(type(bed_time))  # <class 'datetime.time'>
    # NOTE: Even if you input from the alarm clock, it gets stored as a datetime.time object. NOT a string.

    # STEP 1: Need to convert datetime.time object to a string
    wake_time = str(wake_time)
    print(type(wake_time))

    bed_time = str(bed_time)
    print(type(bed_time))

    # STEP 1:
    wake_time = datetime.strptime(
        wake_time, "%H:%M:%S"
    )  # Wake time must be a STRING, not a datetime.time object when using strptime() argument
    print("WAKE TIME:", wake_time)

    wake_time_obj = datetime.time(wake_time)
    print("WAKE TIME OBJECT", wake_time_obj)

    bed_time = datetime.strptime(bed_time, "%H:%M:%S")
    print("Bed TIME:", bed_time)

    bed_time_obj = datetime.time(bed_time)
    print("BED TIME OBJECT", bed_time_obj)

    print()
    date_time_wake = datetime.combine(
        date_timez, wake_time_obj
    )  # These need to both be objects!
    print("DATE WAKE", date_time_wake)
    time_wake_obj = datetime.time(date_time_wake)
    print("NEW TIME WAKE", time_wake_obj)
    # wake_time_obj = datetime.strptime(date_time_wake, format)

    print()
    date_time_bed = datetime.combine(date_timez, bed_time_obj)
    print("DATE BED", date_time_bed)
    time_bed_obj = datetime.time(date_time_bed)
    print("NEW TIME BED", time_bed_obj)
    # bed_time_obj = datetime.strptime(date_time_bed, format)
    # print("THE BED TIME OBJECT IS", bed_time_obj)
    print()
    timeStr_wake = time_wake_obj.strftime("%H:%M:%S")
    print("String WAKE", timeStr_wake)
    timeStr_bed = time_bed_obj.strftime("%H:%M:%S")
    print("String BED", timeStr_bed)

    # Get the difference between datetimes (as timedelta)
    date_time_difference = datetime.strptime(timeStr_wake, format) - datetime.strptime(
        timeStr_bed, format
    )

    print()
    print("TIME DIFFERENCE?", date_time_difference)  # -1 day, 8:00:00 ; TIMEDELTA
    print()

    days, seconds = date_time_difference.days, date_time_difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    print(f"{hours} hours and {minutes} minutes")

    # Divide difference in seconds by number of seconds in hour (3600)
    # date_time_difference_in_hours = date_time_difference.total_seconds() / 3600
    # print("THE SUBTRACT time is", date_time_difference_in_hours)
    time_diff = f"{hours}.{minutes}"
    time_diff = float(time_diff)
    print("FLOAT Time difference", time_diff)

    return time_diff


# ===============================================
# HYPNOGRAM Starts Here:


def create_hypnogram(total_sleep_hours):
    """Return dictionary with 4 sleep stages"""

    # Notes for dictionary keys:
    # Awake = awake
    # Stage 1 = NREM1
    # Stage 2 = NREM2
    # Stage 3/4 = NREM3
    # REM = 4

    # Total sleep time is 4 hrs or 240min
    total_sleep_min = total_sleep_hours * 60
    print("Your TOTAL SLEEP in MIN:", total_sleep_min)

    # Sleep cycles last about 90 min?
    sleep_cycle = total_sleep_min // 90
    print("Your NUMBER of sleep cycle is:", sleep_cycle)

    time_dict = {}

    i = 0
    while i < sleep_cycle:

        # ONE CYCLE: After this, the cycle should not include Stage 1
        if i < 1:
            awake_stage = randint(12, 15)
            print("Awake time stage is", awake_stage)

            time_dict["awake"] = [awake_stage]

            # ======================================================================================

            time_dict["REM"] = [10]

            # ======================================================================================
            stage_1 = randint(5, 10)
            print("Stage 1 sleep time is", stage_1)

            time_dict["NREM1"] = stage_1

            # ======================================================================================
            stage_2 = randint(10, 25)
            print("Stage 2 sleep time is", stage_2)

            time_dict["NREM2"] = [stage_2]

            # ======================================================================================

            # stage_3_4 = randint(20, 40)
            # print("Stage 3 and 4 sleep time is", stage_3_4)

            # time_dict["NREM3"] = [stage_3_4]

            total_sleep_before_rem = awake_stage + stage_1 + stage_2 + 10
            print("Total Sleep Before REM", total_sleep_before_rem)

            # Every cycle is about 90 min before REM initiates
            time_difference_before_rem_stage = 90 - total_sleep_before_rem
            print(
                "Sleep difference before REM initiates, which will be stage 3 and 4",
                time_difference_before_rem_stage,
            )

            time_dict["NREM3"] = [time_difference_before_rem_stage]

            # total_stage_3_4_time = time_difference_before_rem_stage + stage_3_4
            # print("Total sleep stage 3 and 4", total_stage_3_4_time)

            # time_dict["NREM3"] = [total_stage_3_4_time]

            # # ======================================================================================

            # final_total_sleep_before_rem = (
            #     awake_stage + stage_1 + stage_2 + total_stage_3_4_time
            # )
            # print("Total Sleep Before REM", final_total_sleep_before_rem)

            # # ======================================================================================
            # # rem_sleep = random.randint(20, 60)
            # print("First stage of REM sleep will be 10min")

            # time_dict["REM"] = [10]

            i += 1

        elif i < (sleep_cycle - 1):

            # awake_stage = randint(12, 15)
            # print("Awake time stage is", awake_stage)

            # time_dict["awake"] = awake_stage

            # ======================================================================================
            # stage_1 = randint(5, 10)
            # print("Stage 1 sleep time is", stage_1)

            # time_dict['NREM1'] = stage_1

            # ======================================================================================
            stage_2 = randint(30, 60)  # SWITCHED TO 20, 40
            print("Stage 2 sleep time is", stage_2)

            time_dict["NREM2"].append(stage_2)

            # ======================================================================================
            stage_3_4 = randint(10, 20)  # SWITCHED FROM 20, 40
            print("Stage 3 and 4 sleep time is", stage_3_4)

            time_dict["NREM3"].append(stage_3_4)

            total_sleep_before_rem = stage_2 + stage_3_4
            print("Total Sleep Before REM", total_sleep_before_rem)

            # Every cycle is about 90 min before REM initiates
            time_difference_before_rem_stage = 90 - total_sleep_before_rem
            print(
                "Sleep difference before REM initiates",
                time_difference_before_rem_stage,
            )

            time_dict["REM"].append(time_difference_before_rem_stage)

            # total_stage_3_4_time = time_difference_before_rem_stage + stage_3_4
            # print("Total sleep stage 3 and 4", total_stage_3_4_time)

            # time_dict["NREM3"].append(total_stage_3_4_time)

            # # ======================================================================================

            # final_total_sleep_before_rem = (
            #     awake_stage + stage_1 + stage_2 + total_stage_3_4_time
            # )
            # print("Total Sleep Before REM", final_total_sleep_before_rem)

            # # ======================================================================================
            # rem_sleep = randint(30, 60)
            # print("First stage of REM sleep will be 10min")

            # time_dict["REM"].append(rem_sleep)

            i += 1

        else:

            awake_stage = randint(12, 15)
            print("Awake time stage is", awake_stage)

            time_dict["awake"].append(awake_stage)

            # ======================================================================================
            # stage_1 = randint(5, 10)
            # print("Stage 1 sleep time is", stage_1)

            # time_dict['NREM1'] = stage_1

            # ======================================================================================
            stage_2 = randint(20, 40)
            print("Stage 2 sleep time is", stage_2)

            time_dict["NREM2"].append(stage_2)

            # ======================================================================================
            stage_3_4 = randint(10, 20)
            print("Stage 3 and 4 sleep time is", stage_3_4)

            time_dict["NREM3"].append(stage_3_4)

            total_sleep_before_rem = awake_stage + stage_2 + stage_3_4
            print("Total Sleep Before REM", total_sleep_before_rem)

            # Every cycle is about 90 min before REM initiates
            time_difference_before_rem_stage = 90 - total_sleep_before_rem
            print(
                "Sleep difference before REM initiates",
                time_difference_before_rem_stage,
            )

            time_dict["REM"].append(time_difference_before_rem_stage)

            # total_stage_3_4_time = time_difference_before_rem_stage + stage_3_4
            # print("Total sleep stage 3 and 4", total_stage_3_4_time)

            # time_dict["NREM3"].append(total_stage_3_4_time)

            # # ======================================================================================

            # final_total_sleep_before_rem = (
            #     awake_stage + stage_1 + stage_2 + total_stage_3_4_time
            # )
            # print("Total Sleep Before REM", final_total_sleep_before_rem)

            # # ======================================================================================
            # rem_sleep = randint(0, 60)
            # print("First stage of REM sleep will be 10min")

            # time_dict["REM"].append(rem_sleep)

            i += 1

    print(time_dict)
    return time_dict


# THIS FUNCTION CHECKS OUT ABOVE!
# ======================================================================================
# THIS FUNCTION CHECKS OUT BELOW


def create_time_stages(time_dict, total_sleep_hours):
    """Return dictionary with sleep stages with sleep time"""

    total_sleep_min = total_sleep_hours * 60
    print("Your TOTAL SLEEP in MIN:", total_sleep_min)

    # Sleep cycles last about 90 min?
    sleep_cycle = total_sleep_min // 90
    print("Your NUMBER of sleep cycle is:", sleep_cycle)

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
            # stage_2.pop((0))

            stage_3 = time_dict.get("NREM3")
            time_stages.append(stage_3[0])
            # stage_3.pop((0))

            rem = time_dict.get("REM")
            time_stages.append(rem[0])
            # rem.pop((0))

            i += 1

        elif i < sleep_cycle - 1:
            print("IF THIS WORKS:", stage_2[i])
            time_stages.append(stage_2[i])
            # stage_2.pop(i)
            time_stages.append(stage_3[i])

            time_stages.append(rem[i])

            i += 1

        else:

            time_stages.append(stage_2[i])
            time_stages.append(stage_3[i])
            time_stages.append(rem[i])
            time_stages.append(awake[0])

            break

    print("The FINAL stage 2 is:", stage_2)
    print("THE TIME STAGE IS:", time_stages)

    return time_stages


# elif i < 4 - 1:


# for indx, num in enumerate(lst):
#     print(indx, num)

# i = 0
# while i < len(lst):
#     print(i)
#     print(lst[i])

#     i += 1

# ======================================================================================
# THIS FUNCTION CHECKS OUT BELOW


def create_total_time_lst(time_stages):
    """Return a list with times adding to total minutes of sleep cycle"""

    time_lst = []

    num = time_stages[0]  # Start at first index; 12
    time_lst.append(num)

    for i in range(len(time_stages) - 1):
        # print(i)
        # new_lst.append(lst[i])  # Add the first element to new list

        next_num = time_stages[i + 1]
        # print(next_num)

        num += next_num
        # print(number)

        time_lst.append(num)

        i += 1

    print()
    print("BEHOLD THE TIME LIST:", time_lst)
    print()
    return time_lst


# ======================================================================================
# THIS FUNCTION CHECKS OUT BELOW


def create_time_final_dict(time_stages, time_lst):
    """"Return dictionary with time stage and time minutes to JSON"""

    print(len(time_stages))
    print(len(time_lst))

    # GIVEN THE TIME LIST, assign values of the time as KEYS to a dictionary. While, the values of those time keys will be the stages
    # time_lst = [14, 19, 40, 80, 90, 110, 136, 180, 195, 235, 270, 284, 311, 348, 360]
    final_time_dict = {}

    sleep_cycle = 4

    # ["Awake", "NREM1", "NREM2", "NREM3", "REM"] #[5, 3, 2, 1, 4]
    first_sleep_stage_lst = [5, 3, 2, 1, 4]
    middle_sleep_stage_lst = [2, 1, 4]  # ["NREM2", "NREM3", "REM"] #[2, 1, 4]
    # ["NREM2", "NREM3", "REM", "Awake"] #[2,1,4,5]
    last_sleep_stage_lst = [2, 1, 4, 5]
    i = 0
    while i < sleep_cycle:

        if i < 1:
            time_lst_first_slice = time_lst[0:5]

            print(time_lst)

            for time_key in time_lst_first_slice:
                for stage_value in first_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    first_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

        elif i < sleep_cycle - 1:

            middle_length = len(middle_sleep_stage_lst)
            print("MIDDLE LENGTH:", middle_length)

            print(type(middle_length))

            time_slice_middle = time_lst[5:]  # KEYS

            slice_length = len(time_slice_middle) - 4
            print("SLICE LENGTH:", slice_length)

            print(type(slice_length))

            new_middle_lst = []

            while middle_length < slice_length:
                for sleep_stage in middle_sleep_stage_lst:
                    new_middle_lst.append(sleep_stage)

                    middle_length += 1

            print(middle_sleep_stage_lst)
            print(new_middle_lst)

            final_middle_sleep_stage_lst = middle_sleep_stage_lst + new_middle_lst
            print(final_middle_sleep_stage_lst)

            for time_key in time_slice_middle:
                for stage_value in final_middle_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    final_middle_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

        else:

            time_lst_last_slice = time_lst[-4:]
            print("NEW MIDDLE TIME SLICE", time_lst_last_slice)

            for time_key in time_lst_last_slice:
                for stage_value in last_sleep_stage_lst:
                    final_time_dict[time_key] = stage_value
                    last_sleep_stage_lst.remove(stage_value)
                    break

            i += 1

    print("THE FINAL TIME DICT is:", final_time_dict)
    return final_time_dict


# ===============================================
# DOUGHNUT CHART DATA CALCULATIONS Starts Here:


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

    # ====================================
    awake = time_dict.get("awake")
    print(awake)  # Gives back a list
    awake_percent = calculate_sleep_stage_percent(awake, total_sleep_time)

    doughnut_dict["Awake"] = awake_percent

    # ====================================LIGHT SLEEP STARTS HERE
    # WILL NEED TO CHANGE IF YOU FIX THE FORMULA FOR THE HYNOGRAM!!!
    stage_1 = time_dict.get("NREM1")
    stage_1_percent = (stage_1 / total_sleep_time) * 100

    stage_2 = time_dict.get("NREM2")
    # time_stages.append(stage_2[0])
    # stage_2.pop((0))
    stage_2_percent = calculate_sleep_stage_percent(stage_2, total_sleep_time)

    doughnut_dict["Light Sleep"] = stage_1_percent + stage_2_percent

    # ====================================DEEP SLEEP STARTS HERE
    stage_3 = time_dict.get("NREM3")
    # time_stages.append(stage_3[0])
    # stage_3.pop((0))
    stage_3_percent = calculate_sleep_stage_percent(stage_3, total_sleep_time)

    doughnut_dict["Deep Sleep"] = stage_3_percent

    rem = time_dict.get("REM")
    rem_percent = calculate_sleep_stage_percent(rem, total_sleep_time)

    doughnut_dict["REM Sleep"] = rem_percent

    return doughnut_dict
