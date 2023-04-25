from os import environ
from datetime import time
from unittest.mock import patch, Mock
import flask_testing
from sqlalchemy.engine.row import Row
from flask_login import FlaskLoginClient
from app.config import Config
from app.app import create_app
from app.extensions.database.models import Lesson, Subject, User
from app.extensions.database.database import db


class TestScheduleRoutesDatabase(flask_testing.TestCase):
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

    def test_schedule_with_db(self):
        user = User(email="testing_schedule@setbox.de", first_name="Testy")
        user.set_password("test_password")

        db.session.add(user)
        db.session.commit()

        subject = Subject(name="Test Subject", owner_user_id=user.id)

        db.session.add(subject)
        db.session.commit()

        lesson_1 = Lesson(
            subject_id=1,
            date="2024-04-24",
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name="Test Lesson 1",
        )

        db.session.add(lesson_1)

        lesson_2 = Lesson(
            subject_id=1,
            date="2024-04-24",
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name=None,
        )

        db.session.add(lesson_2)
        db.session.commit()

        with self.app.test_client(user=user) as client:
            response = client.get("/schedule/2024-04-24")
        assert response.status_code == 200
        assert b"16:00:00" in response.data
        assert b"17:00:00" in response.data
        assert b"Test Lesson 1" in response.data
        assert b"Test Subject" in response.data


class TestScheduleRoutesMock(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        app = create_app(self.config())
        return app

    def setUp(self):
        self.app = self.create_app()
        self.app.test_client_class = FlaskLoginClient

    @patch("app.schedule.routes.db")
    def test_schedule_with_mock(self, mock_db):
        mock_user = User(id=1, email="testing_schedule@setbox.de", first_name="Testy")
        mock_user.set_password("test_password")
        mock_subject = Subject(id=1, name="Test Subject", owner_user_id=1)
        mock_row_lesson_1 = Mock(spec=Row)
        mock_lesson_1 = Lesson(
            subject_id=1,
            date="2024-04-24",
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name="Test Lesson 1",
        )
        mock_row_lesson_1.Lesson = mock_lesson_1
        mock_row_lesson_1.Lesson.id = 1
        mock_row_lesson_1.Lesson.formatted_date = "24.04.2024"
        mock_row_lesson_1.Subject = mock_subject

        mock_row_lesson_2 = Mock(spec=Row)
        mock_lesson_2 = Lesson(
            subject_id=1,
            date="2024-04-24",
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name=None,
        )
        mock_row_lesson_2.Lesson = mock_lesson_2
        mock_row_lesson_2.Lesson.id = 2
        mock_row_lesson_2.Lesson.formatted_date = "24.04.2024"
        mock_row_lesson_2.Subject = mock_subject

        mock_db.session.query.return_value.filter.return_value.filter.return_value.join.return_value.filter.return_value.all.return_value = [
            mock_row_lesson_1,
            mock_row_lesson_2,
        ]
        with self.app.test_client(user=mock_user) as client:
            response = client.get("/schedule/2024-04-24")
        print(response.data)
        assert response.status_code == 200
        assert b"16:00:00" in response.data
        assert b"17:00:00" in response.data
        assert b"Test Lesson 1" in response.data
        assert b"Test Subject" in response.data
