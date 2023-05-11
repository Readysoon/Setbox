from os import environ
from datetime import time
import flask_testing
from flask_login import FlaskLoginClient
from AdvancedHTMLParser import AdvancedHTMLParser
from unittest.mock import patch, Mock
from sqlalchemy.engine.row import Row
from werkzeug.security import generate_password_hash
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

        parser = AdvancedHTMLParser()

        with self.app.test_client(user=user) as client:
            response = client.get("/schedule/2024-04-24")

        parser.parseStr(response.text)

        body_element = parser.body
        table_element = parser.getElementsByTagName("table")[0]

        assert response.status_code == 200
        assert "16:00:00" in body_element.innerHTML
        assert "17:00:00" in body_element.innerHTML
        assert "Test Lesson 1" in body_element.innerHTML
        assert "Test Subject" in body_element.innerHTML
        assert "None" not in body_element.innerHTML
        assert "16:00:00" in table_element.innerHTML
        assert "17:00:00" in table_element.innerHTML
        assert "Test Subject" in table_element.innerHTML
        assert "Test Lesson 1" in table_element.innerHTML



class TestScheduleRoutesMock(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        app = create_app(self.config())
        app.test_client_class = FlaskLoginClient
        return app

    @patch("app.schedule.routes.lesson_controller")
    @patch("app.extensions.authentication.User")
    def test_schedule_with_mock(self, mock_user, mock_lesson_controller):
        mock_user = User(
            id=1,
            email="test@test.de",
            password=generate_password_hash("test_password"),
            first_name="Test",
        )
        mock_subject = Mock(spec=Subject)
        mock_lesson = Mock(spec=Lesson)
        mock_lesson.name = "Test Lesson"
        mock_lesson.start_time = time(16, 0)
        mock_lesson.end_time = time(17, 0)
        mock_lesson.formatted_date = "24.04.2024"
        mock_row = Mock(spec=Row)
        mock_row.Lesson = mock_lesson
        mock_row.Subject = mock_subject
        mock_lesson_controller.get_all_lessons_with_subjects_within_dates.return_value = (
            [mock_row]
        )
        with self.app.test_client(user=mock_user) as client:
            response = client.get("/schedule/2024-04-24")

        parser = AdvancedHTMLParser()

        parser.parseStr(response.text)

        body_element = parser.body
        table_element = parser.getElementsByTagName("table")[0]

        assert response.status_code == 200
        assert "16:00:00" in body_element.innerHTML
        assert "17:00:00" in body_element.innerHTML
        assert "Test Lesson" in body_element.innerHTML
        assert "Test Subject" not in body_element.innerHTML
        assert "None" not in body_element.innerHTML
        assert "16:00:00" in table_element.innerHTML
        assert "17:00:00" in table_element.innerHTML
        assert "Test Lesson" in table_element.innerHTML
        
