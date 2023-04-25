from sqlalchemy.orm import column_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions.database.database import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(1024), nullable=False)
    first_name = db.Column(db.VARCHAR(50), nullable=False)
    user_in_subjects = db.relationship("UserInSubject", backref="users", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_in_subjects = db.relationship(
        "UserInSubject", backref="subjects", lazy=True, cascade="all, delete"
    )
    lessons = db.relationship(
        "Lesson", backref="subjects", lazy=True, cascade="all, delete"
    )
    __table_args__ = (
        db.UniqueConstraint("name", "owner_user_id", name="_name_for_owner"),
    )


class Lesson(db.Model):
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    formatted_date = column_property(db.func.to_char(date, "dd.mm.yyyy"))
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    name = db.Column(db.VARCHAR(255))
    files = db.relationship("File", backref="lessons", lazy=True, cascade="all, delete")


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    type = db.Column(db.VARCHAR(20))
    filename = db.Column(db.VARCHAR(255), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), nullable=False)
    reviewed = db.Column(db.Boolean, nullable=False, default=False)


class UserInSubject(db.Model):
    __tablename__ = "users_in_subjects"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), primary_key=True)
    editor = db.Column(db.Boolean, nullable=False)
