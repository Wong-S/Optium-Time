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
    utc_datetime = datetime.now(user_timezone)
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

