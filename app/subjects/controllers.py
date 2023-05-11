from sqlalchemy import func, case
from sqlalchemy.sql.expression import and_, or_
from app.extensions.database.database import db
from app.extensions.database.models import Subject, User, UserInSubject, File, Lesson


class SubjectController:
    def create_subject(self, subject_name, user_id):
        subject = Subject(name=subject_name, owner_user_id=user_id)
        db.session.add(subject)
        db.session.commit()
        return subject

    def get_all_user_subjects(self, user_id):
        all_user_subjects = (
            Subject.query.join(User, isouter=True).filter(User.id == user_id).all()
        )
        return all_user_subjects

    def get_all_shared_subjects(self, user_id):
        all_shared_subjects = (
            Subject.query.join(UserInSubject, isouter=True)
            .filter(UserInSubject.user_id == user_id)
            .all()
        )
        return all_shared_subjects

    def get_subject_by_id(self, subject_id):
        subject = Subject.query.filter(Subject.id == subject_id).first()
        return subject

    def check_if_user_owns_subject(self, subject_id, user_id):
        subject = self.get_subject_by_id(subject_id)
        if user_id == subject.owner_user_id:
            return True
        return False

    def find_if_subject_is_shared(self, subject_id, user_id):
        query = (
            UserInSubject.query.join(Subject, isouter=True)
            .join(User, isouter=True)
            .filter(Subject.id == subject_id)
            .filter(User.id == user_id)
            .first()
        )
        if query != None:
            return True
        return False

    def check_if_user_can_access_subject(self, subject_id, user_id):
        subject = self.get_subject_by_id(subject_id)
        if self.check_if_user_owns_subject or self.find_if_subject_is_shared(
            subject.id, user_id
        ):
            return True
        return False

    def calculate_percentage_with_files(self):
        make_reviewed_into_1 = case((File.reviewed, 1))
        percentage = case(
            (
                func.count(File.reviewed) > 0,
                func.round(
                    (
                        100
                        * func.count(make_reviewed_into_1)
                        / func.count(File.reviewed)
                    ),
                    0,
                ),
            ),
            else_=0,
        )
        return percentage

    def find_subject_progress(self, subject_id):
        # find percentage of files of the subject that are in
        # the reviewed state
        subject_progress_query = (
            db.session.query((self.calculate_percentage_with_files()).label("progress"))
            .join(Lesson, isouter=True)
            .join(Subject, isouter=True)
            .filter(Subject.id == subject_id)
            .first()
        )
        if subject_progress_query.progress == None:
            return 0
        return subject_progress_query.progress

    def find_all_lessons_in_subject_and_their_progress(self, subject_id):
        lessons = (
            db.session.query(
                (self.calculate_percentage_with_files()).label("progress"),
                func.count(File.reviewed == True).label("files"),
                Lesson,
            )
            .join(Lesson, full=True)
            .join(Subject, isouter=True)
            .filter(Subject.id == subject_id)
            .group_by(Lesson.id)
            .order_by(Lesson.date.desc())
            .all()
        )
        return lessons

    def find_all_subjects_owned_or_editor(self, user_id):
        return (
            Subject.query.join(UserInSubject, isouter=True)
            .filter(
                or_(
                    Subject.owner_user_id == user_id,
                    and_(
                        UserInSubject.user_id == user_id,
                        UserInSubject.editor == True,
                    ),
                )
            )
            .all()
        )

    def check_if_user_is_owner_or_editor(self, subject_id, user_id):
        subject = self.get_subject_by_id(subject_id)
        if subject.owner_user_id == user_id:
            return True
        if self.find_if_subject_is_shared(subject_id, user_id):
            user_in_subject = (
                UserInSubject.query.filter(UserInSubject.user_id == user_id)
                .filter(UserInSubject.subject_id == subject_id)
                .first()
            )
            if user_in_subject.editor:
                return True
        return False
