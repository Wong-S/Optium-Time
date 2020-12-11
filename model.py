from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///sleeps", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(30), unique=True)
    timezone = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id = {self.user_id} first_name = {self.first_name}>"


class Journal(db.Model):
    """A journal"""

    __tablename__ = "journals"

    journal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    entry_name = db.Column(db.String(50))
    entry_details = db.Column(db.String)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

    user = db.relationship("User", backref="journals")

    def __repr__(self):
        return f"<Journal journal_id = {self.journal_id} user_id = {self.user_id} entry_name = {self.entry_name} created_at = {self.created_at} updated_at = {self.updated_at}>"


class SleepLog(db.Model):
    """A user's sleep log"""

    __tablename__ = "sleep_logs"

    sleep_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    wake_time = db.Column(db.Time)
    bed_time = db.Column(db.Time)
    current_date = db.Column(db.Date)

    user = db.relationship("User", backref="sleep_logs")

    def __repr__(self):
        return f"<SleepLog sleep_log_id = {self.sleep_log_id} wake_time = {self.wake_time} bed_time = {self.bed_time} current_date = {self.current_date}>"


class Playlist(db.Model):
    """A user's playlist"""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    playlist_name = db.Column(db.String(50))

    user = db.relationship("User", backref="playlists")

    def __repr__(self):
        return f"<Playlist playlist_id = {self.playlist_id} playlist_name = {self.playlist_name}>"


class Video(db.Model):
    """A video from API"""

    __tablename__ = "videos"

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    video_title = db.Column(db.String)
    video_duration = db.Column(db.String)
    video_url = db.Column(db.String)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"))

    playlist = db.relationship("Playlist", backref="videos")

    def __repr__(self):
        return f"<Video video_id = {self.video_id} video_title = {self.video_title} video_url = {self.video_url}>"


class Category(db.Model):
    """Category based on the video"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category_name = db.Column(db.String(30))

    def __repr__(self):
        return f"<Category category_id = {self.category_id} category_name = {self.category_name}>"


class VideoCategories(db.Model):
    """Middle table between Video and Category class"""

    __tablename__ = "videos_categories"

    video_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))

    video = db.relationship("Video", backref="videos_categories")
    category = db.relationship("Category", backref="videos_categories")

    def __repr__(self):
        return f"<VideoCategories video_category_id = {self.video_category_id} video = {self.video} category = {self.category}>"


if __name__ == "__main__":
    from server import app

    connect_to_db(app)

