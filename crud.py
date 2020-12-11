"""CRUD operations"""
from datetime import datetime, time

import YouTube
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
def create_user(first_name, last_name, email, password, timezone):
    """Create and return a new user"""

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        timezone=timezone,
    )

    db.session.add(user)
    db.session.commit()

    return user


# =================================================================
def get_user():
    """Return list of user objects"""

    return User.query.all()


def get_user_by_id(user_id):
    """Return user's profile with user's email"""

    user_by_id = User.query.get(user_id)

    return user_by_id


def get_user_by_email(email):
    """ Return user's profile or None """

    return User.query.filter(User.email == email).first()


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
def create_journal_entry(user_id, entry_name, entry_details, created_at, updated_at):
    """Create and return a new journal entry"""

    journal = Journal(
        user_id=user_id,
        entry_name=entry_name,
        entry_details=entry_details,
        created_at=created_at,
        updated_at=updated_at,
    )

    db.session.add(journal)
    db.session.commit()

    return journal


def get_user_journal(user_id):
    """Return journal list of objects if email matches"""

    user_by_id = User.query.get(user_id)
    return Journal.query.all()


def check_user_to_journal_id(user_id):
    """Return joinedload user objects joined with journal table"""

    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("journals"))
        .first()
    )


# ================================================================
def create_category(category_name):
    """Create and return a new category"""

    category = Category(category_name=category_name)

    db.session.add(category)
    db.session.commit(category)

    return category


def create_video_categories(video_id, category_id):
    """Create and return a new video with category id associated"""

    video_category = VideoCategories(video_id=video_id, category_id=category_id)

    db.session.add(video_category)
    db.session.commit(video_category)

    return video_category


def create_playlist(playlist_name, user_id):
    """Create and return a new playlist"""

    playlist = Playlist(playlist_name=playlist_name, user_id=user_id)

    db.session.add(playlist)
    db.session.commit()

    return playlist


######################################################################
def create_video(video_title, video_duration, video_url, playlist_id):
    """Create and return a new video to a playlist"""

    video = Video(
        video_title=video_title,
        video_duration=video_duration,
        video_url=video_url,
        playlist_id=playlist_id,
    )

    db.session.add(video)
    db.session.commit()

    return video


######################################################################
def display_selected_videos(video_category, video_duration):
    """Return list of selected video attributes"""

    selected_video = YouTube.search_videos(video_category, video_duration)

    return selected_video


def check_user_to_playlist_id(user_id):
    """Return joinedload user objects joined with playlists table"""

    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("playlists"))
        .first()
    )


def get_videos_from_playlist_id(playlist_id):
    """Return joinedload video objects joined with playlists table"""

    return (
        Playlist.query.filter(Playlist.playlist_id == playlist_id)
        .options(db.joinedload("videos"))
        .first()
    )


# ================================================================
def create_sleep_log(user_id, wake_time, bed_time, current_date):
    """Create and return a new sleep log entry"""

    sleep_log = SleepLog(
        user_id=user_id,
        wake_time=wake_time,
        bed_time=bed_time,
        current_date=current_date,
    )

    db.session.add(sleep_log)
    db.session.commit()

    return sleep_log


def get_sleep_data_user_id(user_id):
    """Return joinedload user objects joined with sleep_logs table"""

    return (
        User.query.filter(User.user_id == user_id)
        .options(db.joinedload("sleep_logs"))
        .first()
    )


def get_sleep_data_by_date(user_id, current_date_lst, correct_date_obj):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    for date in user_id_sleep_log_obj.sleep_logs:
        if correct_date_obj in current_date_lst:
            return SleepLog.query.filter(
                SleepLog.current_date == correct_date_obj
            ).first()


def get_sleep_data_by_filtered_date(user_id, chosen_date_by_user):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    for date in user_id_sleep_log_obj.sleep_logs:
        if chosen_date_by_user == date.current_date:
            return SleepLog.query.filter(
                SleepLog.current_date == chosen_date_by_user
            ).first()


def get_sleep_time_by_filtered_date_lst(user_id, date_obj_lst):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    selected_date_obj_lst = []
    for all_dates in user_id_sleep_log_obj.sleep_logs:
        for date_lst in date_obj_lst:
            for date_obj in date_lst:

                if date_obj == all_dates.current_date:

                    query_obj = SleepLog.query.filter(
                        SleepLog.current_date == date_obj
                    ).first()

                    selected_date_obj_lst.append(query_obj)

    return selected_date_obj_lst


def get_sleep_time_by_filtered_month_lst(user_id, month_date_obj_lst):
    """Return sleep log objects filtering for current date"""

    user_id_sleep_log_obj = get_sleep_data_user_id(user_id)

    selected_date_obj_lst = []
    for all_dates in user_id_sleep_log_obj.sleep_logs:
        for date_in_lst in month_date_obj_lst:
            if all_dates.current_date == date_in_lst:
                query_obj = SleepLog.query.filter(
                    SleepLog.current_date == all_dates.current_date
                ).first()

                selected_date_obj_lst.append(query_obj)

    return selected_date_obj_lst


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
