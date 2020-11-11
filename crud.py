"""CRUD operations"""
from datetime import datetime, time

# FIXME NOTE: Since taking things from model, would be best to import all from model?
# NOTE: CRUD -> create, read, update, delete
from model import (
    db,
    User,
    Journal,
    SleepLog,
    Playlist,
    Video,
    Category,
    VideoCategories,
    connect_to_db,
)

# =================================================================
# CREATE USER TABLE, link to Model.py
# NOTE: 'first_name' must be same as called in model.py Class
# Part 1: Create user
def create_user(first_name, last_name, email, password):
    """Create and return a new user"""

    user = User(
        first_name=first_name, last_name=last_name, email=email, password=password
    )

    db.session.add(user)
    db.session.commit()

    return user


# NOTE --> Email and Password are Unique!
# Test run in interactive mode:
# create_user('F','L', 'test@.com','124')


# NOTE: CHECKING functions display user emails that were added!

# =================================================================
# USER SECTION:
# Server.py create account POST function
def get_user():
    """Return list of user objects"""

    return User.query.all()


# NOTE: Getting list of objects from class User

# NOTE: Test interactively returns list of user objects


def get_user_by_id(user_id):
    """Return user's profile with user's email"""

    user_by_id = User.query.get(user_id)

    return user_by_id


# NOTE: This returns at that specific id key for that user, with their info like name, email, etc. That you can make an instance attribute, etc
# <User user_id 1 first_name = David >


def get_user_by_email(email):
    """ Return user's profile or None """

    return User.query.filter(User.email == email).first()


# Server.py login route:
def check_password(email, password):
    """ Compare password on file for a user when they are logging in"""

    user_info = get_user_by_email(email)

    if user_info == None:
        return False
    elif user_info.password == password:
        return True
    else:
        return False


# ================================================================
# JOURNAL SECTION:

# Part 2:
# Create a Journal entry for user:
def create_journal_entry(
    user_id,
    entry_name,
    entry_details,
    created_at=datetime.now(),
    updated_at=datetime.now(),
):
    """Create and return a new journal entry"""

    journal = Journal(
        user_id=user_id,
        entry_name=entry_name,
        entry_details=entry_details,
        created_at=datetime.date(created_at),
        updated_at=datetime.date(updated_at),
        # NOTE: Foreign Key from User Table
    )

    db.session.add(journal)
    db.session.commit()

    return journal


# NOTE --> Need datetime.now() for when the exact moment created_at and updated_at occur. Might need to revise created_at to be fixed.
# Test run in interactive mode:
# 1) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020', '31-Oct-2020')
# OR:
# 2) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020', None)
# OR:
# 3) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove', '31-Oct-2020')
# OR:
# 4) --> create_journal_entry('Kitchen Fire', 'Piece of parchment paper was set ablaze while touching the hot stove')


def get_user_journal(user_id):
    """Return journal list of objects if email matches"""

    user_by_id = User.query.get(user_id)
    return Journal.query.all()


def check_user_to_journal_id(user_id):
    """Return joinedload user objects joined with journal table"""

    # user_id = int(user_id)
    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("journals"))
        .first()
    )


# ================================================================
# PLAYLIST--VIDEO SECTION:
# Part 3:

# Create a Playlist
def create_playlist(playlist_name, user_id):
    """Create and return a new playlist"""

    playlist = Playlist(playlist_name=playlist_name, user_id=user_id)

    db.session.add(playlist)
    db.session.commit()

    return playlist


######################################################################

# Create a Video


def create_video(playlist_id, description, duration, video_url):
    """Create and return a new video to a playlist"""

    video = Video(
        playlist_id=playlist_id,
        description=description,
        duration=duration,
        video_url=video_url,
    )

    db.session.add(video)

    db.session.commit()

    return video


# ================================================================
# SLEEP LOG SECTION
# Part 4:

# Create a Sleep Log entry for user: FIXME: variable fix
# def create_sleep_log(wake_time, bed_time=datetime.now(), current_date=datetime.now()):
#     """Create and return a new sleep log entry"""

#     sleep_log = SleepLog(
#         wake_time=wake_time
#         bed_time=str(bed_time[11:16]),
#         current_date=datetime.date(current_date),
#     )
# #bed_time=bed_time.strftime("%H:%M")
#     db.session.add(sleep_log)
#     db.session.commit()

#     return sleep_log


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
