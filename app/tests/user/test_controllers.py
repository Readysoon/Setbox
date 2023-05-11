from os import environ
import flask_testing
from app.config import Config
from app.app import create_app
from app.extensions.database.database import db
from app.extensions.database.models import User, Subject, UserInSubject
from app.user.controllers import UserController

user_controller = UserController()


class TestSubjectControllersWithDatabase(flask_testing.TestCase):
    def config(self):
        return Config(database_url=environ.get("TESTING_DATABASE_URL"), testing=True)

    def create_app(self):
        app = create_app(self.config())
        return app

    def setUp(self):
        db.create_all()
        with self.app.app_context():
            user3 = User(id=3, email="test_email@setbox.de", first_name="Testy")
            user3.set_password("test_password")
            db.session.add(user3)
            db.session.commit()
            subject = Subject(id=1, name="Test Subject", owner_user_id=3)
            db.session.add(subject)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_user_by_email(self):
        user = user_controller.get_user_by_email("test_email@setbox.de")
        assert user != None
        assert user.id == 3

    def test_add_user(self):
        user_controller.add_user("testy_email@setbox.de", "test_password", "Testyy")
        user_in_db = User.query.filter(User.email == "testy_email@setbox.de").first()
        assert user_in_db != None

    def test_add_user_in_subject(self):
        user4 = User(id=4, email="testyy_email@setbox.de", first_name="Testyy")
        user4.set_password("test_password")

        db.session.add(user4)
        db.session.commit()

        user_controller.add_user_in_subject(4, 1, True)

        user_in_subject = (
            UserInSubject.query.filter_by(user_id=4).filter_by(subject_id=1).first()
        )
        assert user_in_subject
        assert user_in_subject.editor

    def test_get_subject_owner(self):
        owner = user_controller.get_subject_owner(1)
        assert owner.id == 3
        assert owner.email == "test_email@setbox.de"

    def test_get_subject_editors(self):
        user4 = User(id=4, email="testyy_email@setbox.de", first_name="Testyy")
        user5 = User(id=5, email="testyyy_email@setbox.de", first_name="Testyyy")

        user4.set_password("test_password")
        user5.set_password("test_password")

        db.session.add(user4)
        db.session.add(user5)
        db.session.commit()

        user_in_subject_4 = UserInSubject(user_id=4, subject_id=1, editor=True)
        user_in_subject_5 = UserInSubject(user_id=5, subject_id=1, editor=False)

        db.session.add(user_in_subject_4)
        db.session.add(user_in_subject_5)
        db.session.commit()

        test_list = user_controller.get_subject_editors(1)

        assert len(test_list) == 1
        assert test_list[0].id == 4

    def test_get_subject_viewers(self):
        user4 = User(id=4, email="testyy_email@setbox.de", first_name="Testyy")
        user5 = User(id=5, email="testyyy_email@setbox.de", first_name="Testyyy")

        user4.set_password("test_password")
        user5.set_password("test_password")

        db.session.add(user4)
        db.session.add(user5)
        db.session.commit()

        user_in_subject_4 = UserInSubject(user_id=4, subject_id=1, editor=True)
        user_in_subject_5 = UserInSubject(user_id=5, subject_id=1, editor=False)

        db.session.add(user_in_subject_4)
        db.session.add(user_in_subject_5)
        db.session.commit()

        test_list = user_controller.get_subject_viewers(1)

        assert len(test_list) == 1
        assert test_list[0].id == 5
