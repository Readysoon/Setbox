from os import environ
import flask_testing
from unittest.mock import Mock
from sqlalchemy.engine.row import Row
from datetime import date, time
from app.config import Config
from app.app import create_app
from app.extensions.database.database import db
from app.extensions.database.models import User, Subject, UserInSubject, Lesson, File
from app.subjects.controllers import SubjectController

subject_controller = SubjectController()


class TestSubjectControllersWithDatabase(flask_testing.TestCase):
    def config(self):
        return Config(database_url=environ.get("TESTING_DATABASE_URL"), testing=True)

    def create_app(self):
        app = create_app(self.config())
        return app
    
    def setUp(self):
        db.create_all()
        with self.app.app_context():
            user3 = User(id = 3, email="test_email@setbox.de", first_name="Testy")
            user3.set_password("test_password")
            user9 = User(id = 9, email="testy_email@setbox.de", first_name="Testy McTesty")
            user9.set_password("test_password")

            db.session.add(user3)
            db.session.add(user9)
            db.session.commit()

            subject5 = Subject(id = 5, name = "Test Subject", owner_user_id = 3)
            subject6 = Subject(id = 6, name = "Testy Subjecty", owner_user_id = 3)
            subject8 = Subject(id = 8, name = "Test Subject 8", owner_user_id = 9)

            db.session.add(subject5)
            db.session.add(subject6)
            db.session.add(subject8)
            db.session.commit()

            user_in_subject1 = UserInSubject(user_id = 3, subject_id = 8, editor = True)
            user_in_subject2 = UserInSubject(user_id = 9, subject_id = 6, editor = False)

            db.session.add(user_in_subject1)
            db.session.add(user_in_subject2)
            db.session.commit()

            lesson1 = Lesson(id = 1, subject_id = 6, date = date(2023, 3, 23), start_time = time(14, 0, 0), end_time = time(16,0,0))
            lesson2 = Lesson(id = 2, subject_id = 6, date = date(2023, 5, 11), start_time = time(14, 5, 5), end_time = time(16,6,4))

            db.session.add(lesson1)
            db.session.add(lesson2)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_create_subject(self):
        with self.app.app_context():
            subject_controller.create_subject("Testyy Subjectyy", 3)

            subject = Subject.query.filter(Subject.name == "Testyy Subjectyy").filter(Subject.owner_user_id == 3).first()
            assert subject is not None

    def test_get_all_user_subjects(self):
        with self.app.app_context():
            test_list = subject_controller.get_all_user_subjects(3)
            assert len(test_list) == 2
            assert test_list[0].name == "Test Subject"
            assert test_list[1].name == "Testy Subjecty"

    def test_get_all_shared_subjects(self):
        with self.app.app_context():
            test_list = subject_controller.get_all_shared_subjects(3)
            assert len(test_list) == 1
            assert test_list[0].name == "Test Subject 8"
    
    def test_get_subject_by_id(self):
        with self.app.app_context():
            subject = subject_controller.get_subject_by_id(8)
            assert subject.name == "Test Subject 8"
            assert subject.owner_user_id == 9

    def test_check_if_user_owns_subject_is_true(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_owns_subject(8, 9)

    def test_check_if_user_owns_subject_is_false(self):
        with self.app.app_context():
            assert not subject_controller.check_if_user_owns_subject(5, 9)

    def test_check_if_user_owns_subject_is_false_shared(self):
        with self.app.app_context():
            assert not subject_controller.check_if_user_owns_subject(8, 3)

    def test_check_if_user_owns_subject_is_false_shared_no_editor(self):
        with self.app.app_context():
            assert not subject_controller.check_if_user_owns_subject(6, 9)

    #fix
    def test_find_if_subject_is_shared_is_true_editor(self):
        with self.app.app_context():
            assert subject_controller.find_if_subject_is_shared(8, 3)

    #fix
    def test_find_if_subject_is_shared_is_true_no_editor(self):
        with self.app.app_context():
            assert subject_controller.find_if_subject_is_shared(6, 9)

    #fix
    def test_find_if_subject_is_shared_is_false_owner(self):
        with self.app.app_context():
            assert not subject_controller.find_if_subject_is_shared(8, 9)

    def test_check_if_user_can_access_subject_true_shared_editor(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_can_access_subject(8, 3)

    def test_check_if_user_can_access_subject_true_owned(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_can_access_subject(8, 9)

    def test_check_if_user_can_access_subject_true_shared_no_editor(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_can_access_subject(6, 9)

    def test_check_if_user_can_access_subject_false(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_can_access_subject(5, 9)

    def test_find_subject_progress(self):
        with self.app.app_context():
            file1 = File(id = 1, name = "Test File 1", type="presentation", filename = "1_20230507211447_test_file.pptx", lesson_id = 1, reviewed = True)
            file2 = File(id = 2, name = "Test File 2", type="presentation", filename = "2_20230507230111_test_file_2.pptx", lesson_id = 1, reviewed = False)
            db.session.add(file1)
            db.session.add(file2)
            db.session.commit()

            assert subject_controller.find_subject_progress(6) == 50

    def test_find_subject_progress_no_files(self):
        with self.app.app_context():
            assert subject_controller.find_subject_progress(6) == 0
        
    def test_find_subject_progress_no_progress(self):
        with self.app.app_context():
            file1 = File(id = 1, name = "Test File 1", type="presentation", filename = "1_20230507211447_test_file.pptx", lesson_id = 1, reviewed = False)
            file2 = File(id = 2, name = "Test File 2", type="presentation", filename = "2_20230507230111_test_file_2.pptx", lesson_id = 1, reviewed = False)
            db.session.add(file1)
            db.session.add(file2)
            db.session.commit()

            assert subject_controller.find_subject_progress(6) == 0

    def test_find_all_lessons_in_subject_and_their_progress(self):
        with self.app.app_context():
            file1 = File(id = 1, name = "Test File 1", type="presentation", filename = "1_20230507211447_test_file.pptx", lesson_id = 1, reviewed = True)
            file2 = File(id = 2, name = "Test File 2", type="presentation", filename = "2_20230507230111_test_file_2.pptx", lesson_id = 1, reviewed = False)
            db.session.add(file1)
            db.session.add(file2)
            db.session.commit()
            
            lessons = subject_controller.find_all_lessons_in_subject_and_their_progress(6)
            assert lessons[0].Lesson.id == 2
            assert lessons[0].progress == 0
            assert lessons[1].Lesson.id == 1
            assert lessons[1].progress == 50

    #needs to be fixed
    def test_find_all_subjects_owned_or_editor(self):
        with self.app.app_context():
            test_list = subject_controller.find_all_subjects_owned_or_editor(3)
            assert len(test_list) == 3

    def test_check_if_user_is_owner_or_editor_owned(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_is_owner_or_editor(5, 3)

    #fix
    def test_check_if_user_is_owner_or_editor_editor(self):
        with self.app.app_context():
            assert subject_controller.check_if_user_is_owner_or_editor(8, 3)
        
    def test_check_if_user_is_owner_or_editor_no_editor(self):
        with self.app.app_context():
            assert not subject_controller.check_if_user_is_owner_or_editor(6, 9)

    def test_check_if_user_is_owner_or_editor_false(self):
        with self.app.app_context():
            assert not subject_controller.check_if_user_is_owner_or_editor(5, 9)
