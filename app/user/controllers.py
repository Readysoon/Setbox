from app.extensions.database.models import User, Subject, UserInSubject
from app.extensions.database.database import db


class UserController:
    def get_user_by_email(self, email):
        return User.query.filter(User.email == email).first()

    def add_user(self, email, password, first_name):
        user = User(email=email, first_name=first_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def add_user_in_subject(self, user_id, subject_id, editor):
        user_in_subject = UserInSubject(
            user_id=user_id, subject_id=subject_id, editor=editor
        )
        db.session.add(user_in_subject)
        db.session.commit()

    def get_subject_owner(self, subject_id):
        return User.query.join(Subject).filter(Subject.id == subject_id).first()

    def get_subject_editors(self, subject_id):
        return (
            User.query.join(UserInSubject)
            .join(Subject)
            .filter(Subject.id == subject_id)
            .filter(UserInSubject.editor is True)
            .all()
        )

    def get_subject_viewers(self, subject_id):
        return (
            User.query.join(UserInSubject)
            .join(Subject)
            .filter(Subject.id == subject_id)
            .filter(UserInSubject.editor is False)
            .all()
        )
