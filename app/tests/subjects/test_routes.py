from datetime import datetime
from os import environ
import flask_testing
from flask_login import FlaskLoginClient
from AdvancedHTMLParser import AdvancedHTMLParser
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

        parser = AdvancedHTMLParser()

        with self.app.test_client(user=user) as client:
            response = client.get("/subject")
        
        parser.parseStr(response.text)

        body_element = parser.body

        assert response.status_code == 200
        assert "Test Subject" in body_element.innerHTML

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

        parser = AdvancedHTMLParser()
        parser.parseStr(response.text)
        body_element = parser.body
        progress_elements = parser.getElementsByClassName("progress")

        assert len(progress_elements) == 1
        assert "50%" in body_element.innerHTML
        assert "No progress yet" in body_element.innerHTML
        assert progress_elements[0].style == "width: 25%"


# with mock?
