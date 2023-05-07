import os
from sqlalchemy.sql.expression import and_
from app.extensions.database.models import Lesson, Subject, File, UserInSubject
from app.extensions.database.database import db
from app.helpers.helpers import Helpers

helpers = Helpers()


class LessonController:
    def create_lesson(self, subject_id, date, start_time, end_time, name=None):
        lesson = Lesson(
            subject_id=subject_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            name=name,
        )
        db.session.add(lesson)
        db.session.commit()
        return lesson

    def delete_lesson(self, lesson):
        db.session.delete(lesson)
        db.session.commit()

    def add_file_to_db(self, name, lesson_id, filename):
        file_type = helpers.get_file_type(filename)
        file = File(filename=filename, name=name, lesson_id=lesson_id, type=file_type)
        db.session.add(file)
        db.session.commit()
        return file

    def get_lesson_by_lesson_id(self, lesson_id):
        return Lesson.query.filter(Lesson.id == lesson_id).first()

    def get_lesson_and_subject_by_lesson_id(self, lesson_id):
        return (
            db.session.query(Lesson, Subject)
            .filter(Subject.id == Lesson.subject_id)
            .filter(Lesson.id == lesson_id)
            .first()
        )

    def get_files_in_lesson(self, lesson_id):
        return (
            File.query.join(Lesson, isouter=True)
            .filter(Lesson.id == lesson_id)
            .order_by(File.id.desc())
            .all()
        )

    def get_file_by_file_id(self, file_id):
        return File.query.filter(File.id == file_id).first()

    def change_file_to_done(self, file_id):
        file = self.get_file_by_file_id(file_id)
        file.reviewed = True
        db.session.commit()

    def change_lesson_name(self, lesson_id, new_name):
        lesson = Lesson.query.filter(Lesson.id == lesson_id).first()
        lesson.name = new_name
        db.session.commit()

    def get_lesson_id_from_file_id(self, file_id):
        return File.query.filter(File.id == file_id).first().lesson_id

    def delete_file(self, file_id):
        file = self.get_file_by_file_id(file_id)
        try:
            os.remove("./files/" + file.filename)
        finally:
            db.session.delete(file)
            db.session.commit()

    def get_all_lessons_with_subjects_within_dates(
        self, date_from, date_until, user_id
    ):
        return (
            db.session.query(Lesson, Subject)
            .filter(and_(Lesson.date >= date_from), (Lesson.date <= date_until))
            .join(Subject)
            .join(UserInSubject, isouter=True)
            .filter(
                (Subject.owner_user_id == user_id) | (UserInSubject.user_id == user_id)
            )
            .order_by(Lesson.start_time)
            .all()
        )
