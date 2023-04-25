from datetime import datetime
from unittest.mock import patch, Mock
from os import environ
import flask_testing
from flask_login import FlaskLoginClient
from sqlalchemy.engine.row import Row
from app.app import create_app
from app.extensions.database.models import User, Subject, Lesson, File
from app.extensions.database.database import db
from app.config import Config


class TestSubjectsRoutesSimple(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        app = create_app(self.config())
        return app

    def test_subject_adding_page_no_login(self):
        response = self.client.get("/add_subject")
        assert response.status_code == 401

    def test_subjects_page_no_login(self):
        response = self.client.get("/subject")
        assert response.status_code == 401


class TestSubjectsRoutesWithDatabase(flask_testing.TestCase):
    def config(self):
        return Config(database_url=environ.get("TESTING_DATABASE_URL"), testing=True)

    def create_app(self):
        app = create_app(self.config())
        app.test_client_class = FlaskLoginClient
        return app

    def setUp(self):
        # self.app = self.create_app()
        # self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_subjects_success_with_db(self):
        user = User(email="test_subjects@setbox.de", first_name="Testy")
        user.set_password("test_password")
        db.session.add(user)
        db.session.commit()
        subject = Subject(name="Test Subject", owner_user_id=user.id)
        db.session.add(subject)
        db.session.commit()
        with self.app.test_client(user=user) as client:
            response = client.get("/subject")
        assert response.status_code == 200
        assert b"Test Subject" in response.data

    def test_subject_progress_with_db(self):
        user = User(email="testing_subject@setbox.de", first_name="SetBox")
        user.set_password("test_password")
        db.session.add(user)
        db.session.commit()
        subject = Subject(name="Test Subject", owner_user_id=user.id)
        db.session.add(subject)
        db.session.commit()
        lesson_1 = Lesson(
            subject_id=subject.id,
            date="2023-02-03",
            start_time="12:00:00",
            end_time="14:00:00",
            name="Test Lesson",
        )
        db.session.add(lesson_1)
        lesson_2 = Lesson(
            subject_id=subject.id,
            date="2023-02-05",
            start_time="12:00:00",
            end_time="14:00:00",
            name="Test Lesson",
        )
        db.session.add(lesson_2)
        db.session.commit()
        file_1 = File(
            name="Test File 1",
            type="Picture",
            filename=str(lesson_1.id)
            + "_"
            + datetime.now().strftime("%Y%m%d%H%M%S")
            + "_test.jpg",
            lesson_id=lesson_1.id,
            reviewed=True,
        )
        db.session.add(file_1)
        file_2 = File(
            name="Test File 2",
            type="Picture",
            filename=str(lesson_1.id)
            + "_"
            + datetime.now().strftime("%Y%m%d%H%M%S")
            + "_test.jpg",
            lesson_id=lesson_1.id,
            reviewed=False,
        )
        db.session.add(file_2)
        file_3 = File(
            name="Test File 3",
            type="Picture",
            filename=str(lesson_2.id)
            + "_"
            + datetime.now().strftime("%Y%m%d%H%M%S")
            + "_test.jpg",
            lesson_id=lesson_2.id,
            reviewed=False,
        )
        db.session.add(file_3)
        file_4 = File(
            name="Test File 4",
            type="Picture",
            filename=str(lesson_2.id)
            + "_"
            + datetime.now().strftime("%Y%m%d%H%M%S")
            + "_test.jpg",
            lesson_id=lesson_2.id,
            reviewed=False,
        )
        db.session.add(file_4)
        db.session.commit()
        with self.app.test_client(user=user) as client:
            response = client.get("/subject/" + str(subject.id))
        assert response.status_code == 200
        assert b"50%" in response.data
        assert b"No progress yet" in response.data
        assert b'<div class="progress" style="width: 25%;"></div>' in response.data


class TestSubjectsRoutesWithMocking(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        return create_app(self.config())

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.app.test_client_class = FlaskLoginClient

    @patch("app.subjects.routes.User")
    @patch("app.subjects.routes.current_user")
    @patch("app.subjects.routes.db")
    @patch("app.subjects.routes.Lesson")
    @patch("app.subjects.routes.Subject")
    def test_subject_with_mock(
        self, mock_subject, mock_lesson, mock_db, mock_current_user, mock_user
    ):
        mock_current_user.id = 1
        mock_subject.query.filter.return_value.first.return_value.owner_user_id = 1
        mock_subject.query.filter.return_value.first.return_value.name = "Test Subject"
        mock_lesson = Lesson(
            subject_id=1,
            date="2023-02-01",
            start_time="16:00:00",
            end_time="17:00:00",
            name="Test Lesson",
        )
        mock_row = Mock(spec=Row)
        mock_row.progress = 80
        mock_row.Lesson = mock_lesson
        #line-too-long
        mock_db.session.query.return_value.join.return_value.filter.return_value.filter.return_value.group_by.return_value.order_by.return_value.all.return_value = [
            mock_row
        ]
        mock_user = User(id=1, email="testing_login@setbox.de", first_name="Test Name")
        mock_user.set_password("test_password")
        with self.app.test_client(user=mock_user) as client:
            response = client.get("/subject/1")
        assert response.status_code == 200
        assert b"Test Subject" in response.data
        assert b"Test Lesson" in response.data
