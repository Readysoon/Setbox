from os import environ
from app.config import Config
from app.app import create_app
from flask_login import FlaskLoginClient
from datetime import date, time
import flask_testing
from app.extensions.database.database import db
from app.extensions.database.models import Lesson, File
from app.lesson.controllers import LessonController
from app.subjects.controllers import SubjectController
from app.user.controllers import UserController

lesson_controller = LessonController()
subject_controller = SubjectController()
user_controller = UserController()

class TestLessonControllerWithDatabase(flask_testing.TestCase):
    def config(self):
        return Config(database_url=environ.get("TESTING_DATABASE_URL"), testing=True)

    def create_app(self):
        app = create_app(self.config())
        app.test_client_class = FlaskLoginClient
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_lesson_create_and_delete(self):
        with self.app.app_context():
            user = user_controller.add_user("test_email@setbox.de", "test_password", "Testy")
            subject = subject_controller.create_subject("Test Subject", user.id)
            lesson = lesson_controller.create_lesson(subject.id, date(2023, 4, 28), time(15, 53), time(16, 53), "Test Lesson")
            lesson_id = lesson.id
            lesson_in_db = lesson_controller.get_lesson_by_lesson_id(lesson_id)
            assert lesson_in_db is not None
            assert lesson_in_db.name == "Test Lesson"
            assert lesson_in_db.date == date(2023, 4, 28)
            assert lesson_in_db.start_time == time(15, 53)
            assert lesson_in_db.end_time == time(16, 53)
            lesson_controller.delete_lesson(lesson)
            lesson_in_db = lesson_controller.get_lesson_by_lesson_id(lesson_id)
            assert lesson_in_db is None

    def test_add_file_to_db(self):
        with self.app.app_context():
            user = user_controller.add_user("test_email@setbox.de", "test_password", "Testy")
            subject = subject_controller.create_subject("Test Subject", user.id)
            lesson = lesson_controller.create_lesson(subject.id, date(2023, 4, 28), time(15, 53), time(16, 53), "Test Lesson")
            file = lesson_controller.add_file_to_db("Test File", lesson.id, "test_file.pptx", "Presentation")
            file_in_db = lesson_controller.get_file_by_file_id(file.id)
            assert file_in_db is not None
            assert file_in_db.name == "Test File"
            assert file_in_db.lesson_id == lesson.id
            assert file_in_db.filename == "test_file.pptx"
            assert file_in_db.type == "Presentation"

    def test_get_lesson_and_subject_by_lesson_id(self):
        with self.app.app_context():
            user = user_controller.add_user("test_email@setbox.de", "test_password", "Testy")
            subject = subject_controller.create_subject("Test Subject", user.id)
            lesson = lesson_controller.create_lesson(subject.id, date(2023, 4, 28), time(15, 53), time(16, 53), "Test Lesson")
            lesson_in_db = lesson_controller.get_lesson_and_subject_by_lesson_id(lesson.id)
            assert lesson_in_db.Subject.id == subject.id
