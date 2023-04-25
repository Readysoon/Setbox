from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import func, case
from flask_login import login_required, current_user
from app.extensions.database.database import db
from app.extensions.database.models import Subject, User, Lesson, File, UserInSubject

blueprint = Blueprint("subjects", __name__)


@blueprint.route("/subject")
@login_required
def all_subjects():
    all_user_subjects = (
        Subject.query.filter(Subject.owner_user_id == User.id)
        .filter(User.id == current_user.id)
        .all()
    )
    all_shared_subjects = (
        Subject.query.filter(Subject.id == UserInSubject.subject_id)
        .filter(UserInSubject.user_id == current_user.id)
        .all()
    )
    return render_template(
        "subjects/subjects_page.html",
        subjects=all_user_subjects,
        shared_subjects=all_shared_subjects,
    )


@blueprint.route("/subject/<subject_id>")
@login_required
def subject_page(subject_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    if (
        current_user.id == subject.owner_user_id
        or find_if_subject_is_shared(subject.id, current_user.id) is True
    ):
        all_lessons_info = find_all_lessons_in_subject(subject.id)
        subject_progress = find_subject_progress(subject.id)
        return render_template(
            "subjects/subject.html",
            subject=subject,
            lessons=all_lessons_info,
            progress=subject_progress,
        )
    return redirect(url_for("subjects.all_subjects"))


def find_if_subject_is_shared(subject_id, user_id):
    query = (
        UserInSubject.query.filter(UserInSubject.subject_id == Subject.id)
        .filter(UserInSubject.user_id == User.id)
        .filter(Subject.id == subject_id)
        .filter(User.id == user_id)
        .first()
    )
    if query is not None:
        return True
    return False


def calculate_percentage_with_files():
    make_reviewed_into_1 = case((File.reviewed, 1))
    percentage = case(
        (
            func.count(File.reviewed) > 0,
            func.round(
                (100 * func.count(make_reviewed_into_1) / func.count(File.reviewed)), 0
            ),
        ),
        else_=0,
    )
    return percentage


def find_all_lessons_in_subject(subject_id):
    lessons = (
        db.session.query((calculate_percentage_with_files()).label("progress"), Lesson)
        .join(Lesson, Lesson.id == File.lesson_id, full=True)
        .filter(Lesson.subject_id == Subject.id)
        .filter(Subject.id == subject_id)
        .group_by(Lesson.id)
        .order_by(Lesson.date.desc())
        .all()
    )
    return lessons


def find_subject_progress(subject_id):
    subject_progress_query = (
        db.session.query((calculate_percentage_with_files()).label("progress"))
        .filter(File.lesson_id == Lesson.id)
        .filter(Lesson.subject_id == Subject.id)
        .filter(Subject.id == subject_id)
        .first()
    )
    if subject_progress_query.progress is None:
        return 0
    return subject_progress_query.progress


@blueprint.get("/add_subject")
@login_required
def addsubject():
    return render_template("subjects/subjectcreator.html")


@blueprint.post("/add_subject")
@login_required
def add_subject_func():
    subject_name = request.form.get("subject_name")
    subject = Subject(name=subject_name, owner_user_id=current_user.id)
    db.session.add(subject)
    db.session.commit()
    start_date_str = request.form.get("start_date")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    selection = request.form.get("frequency")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    subject_id = (
        Subject.query.filter(Subject.name == subject_name)
        .filter(Subject.owner_user_id == current_user.id)
        .first()
        .id
    )
    if selection == "1x":
        lesson = Lesson(
            subject_id=subject_id,
            date=start_date,
            start_time=start_time,
            end_time=end_time,
        )
        db.session.add(lesson)
    elif selection == "weekly":
        end_date_str = request.form.get("end_date")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        delta = end_date - start_date
        for days in range(0, delta.days + 1, 7):
            date = start_date + timedelta(days=days)
            lesson = Lesson(
                subject_id=subject_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
            db.session.add(lesson)
    elif selection == "monthly":
        end_date_str = request.form.get("end_date")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        delta = end_date - start_date
        for days in range(delta.days + 1):
            date = start_date + timedelta(days=days)
            if date.strftime("%-d") == start_date.strftime("%-d"):
                lesson = Lesson(
                    subject_id=subject_id,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                )
                db.session.add(lesson)
    db.session.commit()
    return redirect(url_for("subjects.all_subjects"))


@blueprint.get("/addusertosubject/<subject_id>")
@login_required
def addusertosubject(subject_id):
    data = Subject.query.filter(Subject.id == subject_id).first()
    admin = (
        User.query.filter(User.id == Subject.owner_user_id)
        .filter(Subject.id == subject_id)
        .first()
    )
    editors = (
        User.query.filter(User.id == UserInSubject.user_id)
        .filter(UserInSubject.subject_id == Subject.id)
        .filter(Subject.id == subject_id)
        .filter(UserInSubject.editor is True)
        .all()
    )
    viewers = (
        User.query.filter(User.id == UserInSubject.user_id)
        .filter(UserInSubject.subject_id == Subject.id)
        .filter(Subject.id == subject_id)
        .filter(UserInSubject.editor is False)
        .all()
    )
    return render_template(
        "subjects/addusertosubject.html",
        subject_names=data,
        subject_id=subject_id,
        admin=admin,
        editors=editors,
        viewers=viewers,
    )


@blueprint.post("/addusertosubject/<subject_id>")
@login_required
def post_usertosubject(subject_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    if current_user.id == subject.owner_user_id:
        email = request.form.get("email")
        user_role = request.form.get("userrole")
        user = User.query.filter(User.email == email).first()
        editor = user_role == "editor"
        user_in_subject = UserInSubject(
            user_id=user.id, subject_id=subject_id, editor=editor
        )
    db.session.add(user_in_subject)
    db.session.commit()
    return redirect(url_for("subjects.addusertosubject", subject_id=subject_id))


@blueprint.post("/delete_subject/<subject_id>")
@login_required
def delete_subject(subject_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("subjects.all_subjects"))
