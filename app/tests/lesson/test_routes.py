from unittest.mock import patch, Mock
from datetime import time, date
import flask_testing
from flask_login import FlaskLoginClient
from werkzeug.security import generate_password_hash
from sqlalchemy.engine.row import Row
from AdvancedHTMLParser import AdvancedHTMLParser
from app.config import Config
from app.app import create_app
from app.extensions.database.models import User, Subject, Lesson, File


class TestLessonControllerWithMocks(flask_testing.TestCase):
    def config(self):
        return Config(testing=True)

    def create_app(self):
        app = create_app(self.config())
        app.test_client_class = FlaskLoginClient
        return app

    @patch("app.extensions.authentication.User")
    @patch("app.lesson.controllers.File")
    @patch("app.lesson.controllers.db")
    def test_lesson_page_no_lesson_name(self, mock_db, mock_File, mock_user):
        mock_user = User(
            id=1,
            email="test@test.de",
            password=generate_password_hash("test_password"),
            first_name="Test",
        )
        mock_subject = Subject(id=1, name="Test Subject", owner_user_id=1)
        mock_lesson = Lesson(
            id=1,
            subject_id=1,
            date=date(2024, 4, 24),
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name=None,
        )
        mock_lesson.formatted_date = "24.04.2024"
        mock_row = Mock(spec=Row)
        mock_row.Lesson = mock_lesson
        mock_row.Subject = mock_subject
        mock_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            mock_row
        )
        mock_file = File(
            id=1,
            name="Test File",
            type="photo/jpg",
            filename="test_file.jpg",
            lesson_id=1,
        )
        mock_File.query.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
            mock_file
        ]

        parser = AdvancedHTMLParser()

        with self.app.test_client(user=mock_user) as client:
            response = client.get("/lesson/1")

        parser.parseStr(response.text)

        body_element = parser.body
        table_element = parser.getElementsByTagName("table")[0]
        heading_element = parser.getElementsByTagName("h2")[0]

        assert "Test Subject" in body_element.innerHTML
        assert "None" not in body_element.innerHTML
        assert "Test File" in body_element.innerHTML
        assert "photo/jpg" in body_element.innerHTML
        assert "Test Subject" not in table_element.innerHTML
        assert "Test File" in table_element.innerHTML
        assert "photo/jpg" in table_element.innerHTML
        assert "Test Subject" in heading_element.innerHTML

    @patch("app.extensions.authentication.User")
    @patch("app.lesson.controllers.File")
    @patch("app.lesson.controllers.db")
    def test_lesson_page(self, mock_db, mock_File, mock_user):
        mock_user = User(
            id=1,
            email="test@test.de",
            password=generate_password_hash("test_password"),
            first_name="Test",
        )
        mock_subject = Subject(id=1, name="Test Subject", owner_user_id=1)
        mock_lesson = Lesson(
            id=1,
            subject_id=1,
            date=date(2024, 4, 24),
            start_time=time(16, 00, 00),
            end_time=time(17, 00, 00),
            name="Test Lesson",
        )
        mock_lesson.formatted_date = "24.04.2024"
        mock_row = Mock(spec=Row)
        mock_row.Lesson = mock_lesson
        mock_row.Subject = mock_subject
        mock_db.session.query.return_value.filter.return_value.filter.return_value.first.return_value = (
            mock_row
        )
        mock_file = File(
            id=1,
            name="Test File",
            type="photo/jpg",
            filename="test_file.jpg",
            lesson_id=1,
        )
        mock_File.query.join.return_value.filter.return_value.order_by.return_value.all.return_value = [
            mock_file
        ]

        parser = AdvancedHTMLParser()

        with self.app.test_client(user=mock_user) as client:
            response = client.get("/lesson/1")

        parser.parseStr(response.text)

        body_element = parser.body
        table_element = parser.getElementsByTagName("table")[0]
        heading_element = parser.getElementsByTagName("h2")[0]

        assert response.status_code == 200
        assert "None" not in body_element.innerHTML
        assert "Test File" in body_element.innerHTML
        assert "photo/jpg" in body_element.innerHTML
        assert "Test Subject" not in table_element.innerHTML
        assert "Test Lesson" not in table_element.innerHTML
        assert "Test File" in table_element.innerHTML
        assert "photo/jpg" in table_element.innerHTML
        assert "Test Subject" in heading_element.innerHTML
        assert "Test Lesson" in heading_element.innerHTML


# test more routes
