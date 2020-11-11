"""Models for Sleep app."""

from datetime import datetime

# import datetime  #FIXME
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# NOTE: needed to change "postgresql:///ratings" to new database name, which i called "journals" for now
def connect_to_db(flask_app, db_uri="postgresql:///sleeps", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


# Class Functions:
class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String)  # nullable=False
    last_name = db.Column(db.String)  # nullable=False
    email = db.Column(db.String, unique=True)  # nullable=True
    password = db.Column(db.String(30), unique=True)  # nullable=False

    # NOTE: For Journal class, can call entry_1.users; For User class, can call lenoard.journal
    # FIXME: Need to change these and put in appropriate classes!

    def __repr__(self):
        return f"<User user_id = {self.user_id} first_name = {self.first_name}>"


# NOTE --> Need to db.session.add() and commit() before an ID key is assigned to the user_id; instead show None
# Test run in interactive mode:
# user_1 = User(first_name = 'M', last_name = 'H', email = 'test@test', password = '123')


class Journal(db.Model):
    """A journal"""

    __tablename__ = "journals"

    journal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    entry_name = db.Column(db.String(50))  # nullable=True
    entry_details = db.Column(db.String)  # nullable=True
    created_at = db.Column(db.DateTime)  # nullable=True
    updated_at = db.Column(db.DateTime)  # nullable=True

    user = db.relationship(
        "User", backref="journals"
    )  # NOTE: This works and not like this in before in User Class: journal = db.relationship("Journal", backref="users")

    def __repr__(self):
        return f"<Journal journal_id = {self.journal_id} user_id = {self.user_id} entry_name = {self.entry_name} created_at = {self.created_at} updated_at = {self.updated_at}>"


# NOTE
# Test run in interactive mode:
# journal_1 = Journal(entry_name = 'Entry 1', entry_details = 'My journaling starts today', created_at = datetime.now(), updated_at = datetime.now())

# Another way using datetime string formating:
# journal_1 = Journal(entry_name = 'Entry 1', entry_details = 'My journaling starts today', created_at = datetime.now(), updated_at = datetime.strptime("31-Oct-2015", "%d-%b-%Y"))


# NOTE NOTE:
# Test Run in Interactive mode using joinedload!
# user_1 = User.query.filter(User.user_id == 13).options(db.joinedload("journals")).first()
# >>> user_1.first_name
# >>> for i in user_1.journals:
# print(i.entry_name)


class SleepLog(db.Model):
    """A user's sleep log"""

    __tablename__ = "sleep_logs"

    sleep_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    wake_time = db.Column(db.String)  # nullable=False
    bed_time = db.Column(db.DateTime)  # nullable=False
    current_date = db.Column(db.DateTime)  # nullable=False

    user = db.relationship("User", backref="sleep_logs")

    def __repr__(self):
        return f"<SleepLog sleep_log_id = {self.sleep_log_id} bed_time = {self.bed_time} current_date = {self.current_date}>"


# NOTE
# Test run in interactive mode:
# sleep_log_1 = SleepLog(bed_time = datetime.now(), wake_time = datetime.now(), current_date = datetime.now())


class Playlist(db.Model):
    """A user's playlist"""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    playlist_name = db.Column(db.String(50))  # nullable=False

    user = db.relationship("User", backref="playlists")

    def __repr__(self):
        return f"<Playlist playlist_id = {self.playlist_id} playlist_name = {self.playlist_name}>"


# NOTE
# Test run in interactive mode:
# playlist_1 = Playlist(playlist_name = 'Rain sounds only')


class Video(db.Model):
    """A video from API"""

    __tablename__ = "videos"

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"))

    video_title = db.Column(db.String)
    # description = db.Column(db.String)  # nullable=True
    duration = db.Column(db.String)  # nullable=False
    video_url = db.Column(db.String)  # nullable=False

    playlist = db.relationship("Playlist", backref="videos")

    def __repr__(self):
        return f"<Video video_id = {self.video_id} video_url = {self.video_url}>"


# NOTE
# Test run in interactive mode:
# video_1 = Video(description = 'Inside a car while it rains', duration = 2, video_url = 'https://etc')


class VideoDuration(db.Model):
    """API video duration (short, medium, long)"""

    __tablename__ = "video_durations"

    video_duration_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))

    duration_length = db.Column(db.String)

    video = db.relationship("Video", backref="video_durations")

    def __repr__(self):
        return f"<VideoDuration video_duration_id = {self.video_duration_id} duration_length = {self.duration_length}>"


class Category(db.Model):
    """Category based on the video"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    category_name = db.Column(db.String(30))  # nullable=False

    def __repr__(self):
        return f"<Category category_id = {self.category_id} category_name = {self.category_name}>"


# NOTE
# Test run in interactive mode:
# category_1 = Category(category_name = 'Rain sounds')


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


# NOTE
# Test run in interactive mode:
# video_category_1 = VideoCategories(video = video_1, category = category_1)

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

