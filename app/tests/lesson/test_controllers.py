from os import environ
from datetime import date, time
from unittest.mock import patch
import flask_testing
from app.config import Config
from app.app import create_app
from app.extensions.database.database import db
from app.extensions.database.models import User, Subject, Lesson, File
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
        return app

    def setUp(self):
        db.create_all()
        with self.app.app_context():
            user = User(id=5, email="test_email@setbox.de", first_name="Testy")
            user.set_password("test_password")
            db.session.add(user)
            db.session.commit()
            subject = Subject(id=7, name="Test Subject", owner_user_id=5)
            db.session.add(subject)
            db.session.commit()
            lesson = Lesson(
                id=9,
                subject_id=7,
                date=date(2023, 4, 28),
                start_time=time(15, 53),
                end_time=time(16, 53),
                name="Test Lesson",
            )
            db.session.add(lesson)
            db.session.commit()
            file = File(
                id=11,
                filename="test_file.pptx",
                name="Test File",
                lesson_id=9,
                type="Presentation",
            )
            db.session.add(file)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_lesson(self):
        with self.app.app_context():
            lesson_controller.create_lesson(
                7, date(2023, 9, 2), time(18, 0), time(19, 30), "Test Lesson New"
            )
            lesson = (
                Lesson.query.filter(Lesson.subject_id == 7)
                .filter(Lesson.name == "Test Lesson New")
                .first()
            )
            assert lesson.formatted_date == "02.09.2023"
            assert lesson.start_time == time(18, 0, 0)
            assert lesson.end_time == time(19, 30, 0)

    @patch("app.helpers.helpers.filetype")
    def test_add_file_to_db(self, mock_filetype):
        with self.app.app_context():
            mock_filetype.guess.return_value.mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            lesson_controller.add_file_to_db(
                "Test File New", 9, "test_presentation.pptx"
            )
            assert (
                File.query.filter(File.lesson_id == 9)
                .filter(File.name == "Test File New")
                .first()
                is not None
            )

    def test_get_lesson_by_lesson_id(self):
        with self.app.app_context():
            lesson_in_db = lesson_controller.get_lesson_by_lesson_id(9)
            assert lesson_in_db is not None
            assert lesson_in_db.name == "Test Lesson"
            assert lesson_in_db.date == date(2023, 4, 28)
            assert lesson_in_db.start_time == time(15, 53)
            assert lesson_in_db.end_time == time(16, 53)

    def test_change_lesson_name(self):
        with self.app.app_context():
            lesson_controller.change_lesson_name(9, "Test Lesson with New Name")
            test_lesson = Lesson.query.get(9)
            assert test_lesson.name == "Test Lesson with New Name"

    def test_lesson_delete(self):
        with self.app.app_context():
            lesson_in_db = Lesson.query.get(9)
            lesson_controller.delete_lesson(lesson_in_db)
            test_lesson = Lesson.query.get(9)
            assert test_lesson is None

    def test_get_file_by_file_id(self):
        with self.app.app_context():
            file_in_db = lesson_controller.get_file_by_file_id(11)
            assert file_in_db is not None
            assert file_in_db.name == "Test File"
            assert file_in_db.lesson_id == 9
            assert file_in_db.filename == "test_file.pptx"
            assert file_in_db.type == "Presentation"

    def test_get_files_in_lesson(self):
        with self.app.app_context():
            files = lesson_controller.get_files_in_lesson(9)
            assert files[0] is not None
            assert files[0].name == "Test File"
            assert len(files) == 1

    def test_get_lesson_and_subject_by_lesson_id(self):
        with self.app.app_context():
            lesson_in_db = lesson_controller.get_lesson_and_subject_by_lesson_id(9)
            assert lesson_in_db.Subject.id == 7

    def test_change_file_to_done(self):
        with self.app.app_context():
            lesson_controller.change_file_to_done(11)
            file = File.query.get(11)
            assert file.reviewed

    def test_get_lesson_id_from_file_id(self):
        with self.app.app_context():
            assert lesson_controller.get_lesson_id_from_file_id(11) == 9

    def test_get_all_lessons_with_subjects_within_dates(self):
        with self.app.app_context():
            fake_user = User(email="testy_email@setbox.de", first_name="Testy")
            fake_user.set_password("test_password")
            db.session.add(fake_user)
            db.session.commit()

            subject_owner_ids = [5, 5, fake_user.id]
            for x in range(3):
                subject = Subject(
                    id=x + 1,
                    name="Test Subject " + str(x + 1),
                    owner_user_id=subject_owner_ids[x],
                )
                db.session.add(subject)
            db.session.commit()

            ids = [1, 1, 3, 2, 2]
            for x in range(5):
                lesson = Lesson(
                    id=x + 1,
                    subject_id=ids[x],
                    date=date(2023, 4, x + 1),
                    start_time=time(15, 53),
                    end_time=time(16, 49),
                    name="Test Lesson " + str(x),
                )
                db.session.add(lesson)
            db.session.commit()

            lessons_return = (
                lesson_controller.get_all_lessons_with_subjects_within_dates(
                    date(2023, 4, 2), date(2023, 4, 4), 5
                )
            )

            assert (Lesson.query.get(1), Subject.query.get(1)) not in lessons_return
            assert (Lesson.query.get(1), Subject.query.get(2)) not in lessons_return
            assert (Lesson.query.get(1), Subject.query.get(3)) not in lessons_return
            assert (Lesson.query.get(2), Subject.query.get(1)) in lessons_return
            assert (Lesson.query.get(2), Subject.query.get(2)) not in lessons_return
            assert (Lesson.query.get(2), Subject.query.get(3)) not in lessons_return
            assert (Lesson.query.get(3), Subject.query.get(1)) not in lessons_return
            assert (Lesson.query.get(3), Subject.query.get(2)) not in lessons_return
            assert (Lesson.query.get(3), Subject.query.get(3)) not in lessons_return
            assert (Lesson.query.get(4), Subject.query.get(1)) not in lessons_return
            assert (Lesson.query.get(4), Subject.query.get(2)) in lessons_return
            assert (Lesson.query.get(4), Subject.query.get(3)) not in lessons_return
            assert (Lesson.query.get(5), Subject.query.get(1)) not in lessons_return
            assert (Lesson.query.get(5), Subject.query.get(2)) not in lessons_return
            assert (Lesson.query.get(5), Subject.query.get(3)) not in lessons_return
