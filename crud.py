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


# Part 2:
# Create a Journal entry for user:
def create_journal_entry(
    entry_name, entry_details, created_at=datetime.now(), updated_at=datetime.now(),
):
    """Create and return a new journal entry"""

    journal = Journal(
        entry_name=entry_name,
        entry_details=entry_details,
        created_at=datetime.date(created_at),
        updated_at=datetime.date(updated_at),
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


# Part 3:
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


# NOTE: CHECKING functions display user emails that were added!


# POST function
def get_user_by_email(email):
    """ Return user's profile"""

    return User.query.filter(User.email == email).first()


# NOTE -->
# Test run in interactive mode:


# Part 3:
# Create a Playlist for user:


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
