from datetime import timedelta
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions.database.database import db
from app.subjects.controllers import SubjectController
from app.lesson.controllers import LessonController
from app.user.controllers import UserController
from app.helpers.helpers import Helpers

blueprint = Blueprint("subjects", __name__)

subject_controller = SubjectController()
lesson_controller = LessonController()
user_controller = UserController()

helpers = Helpers()


@blueprint.route("/subject")
@login_required
def all_subjects():
    return render_template(
        "subjects/subjects_page.html",
        subjects=subject_controller.get_all_user_subjects(current_user.id),
        shared_subjects=subject_controller.get_all_shared_subjects(current_user.id),
    )


@blueprint.route("/subject/<subject_id>")
@login_required
def subject_page(subject_id):
    if (
        subject_controller.check_if_user_can_access_subject(subject_id, current_user.id)
        is True
    ):
        return render_template(
            "subjects/subject.html",
            subject=subject_controller.get_subject_by_id(subject_id),
            lessons=subject_controller.find_all_lessons_in_subject_and_their_progress(
                subject_id
            ),
            progress=subject_controller.find_subject_progress(subject_id),
        )
    return redirect(url_for("subjects.all_subjects"))


@blueprint.get("/add_subject")
@login_required
def addsubject():
    return render_template("subjects/subjectcreator.html")


@blueprint.post("/add_subject")
@login_required
def add_subject_func():
    subject_name = request.form.get("subject_name")
    start_date = helpers.make_string_into_date(request.form.get("start_date"))
    end_date = helpers.make_string_into_date(request.form.get("end_date"))
    selection = request.form.get("frequency")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    subject = subject_controller.create_subject(subject_name, current_user.id)
    if selection == "1x":
        lesson_controller.create_lesson(subject.id, start_date, start_time, end_time)
    else:
        delta = end_date - start_date
        for days in range(0, delta.days + 1, int(selection)):
            date = start_date + timedelta(days=days)
            lesson_controller.create_lesson(subject.id, date, start_time, end_time)
    db.session.commit()
    return redirect(url_for("subjects.all_subjects"))


@blueprint.get("/addusertosubject/<subject_id>")
@login_required
def addusertosubject(subject_id):
    return render_template(
        "subjects/addusertosubject.html",
        subject=subject_controller.get_subject_by_id(subject_id),
        admin=user_controller.get_subject_owner(subject_id),
        editors=user_controller.get_subject_editors(subject_id),
        viewers=user_controller.get_subject_viewers(subject_id),
    )


@blueprint.post("/addusertosubject/<subject_id>")
@login_required
def post_usertosubject(subject_id):
    subject = subject_controller.get_subject_by_id(subject_id)
    if subject_controller.check_if_user_owns_subject(subject.id, current_user.id):
        email = request.form.get("email")
        user_role = request.form.get("userrole")
        user = user_controller.get_user_by_email(email)
        editor = user_role == "editor"
        if user.id != current_user.id:
            if user is not None:
                user_controller.add_user_in_subject(user.id, subject.id, editor)
    return redirect(url_for("subjects.addusertosubject", subject_id=subject_id))


@blueprint.post("/delete_subject/<subject_id>")
@login_required
def delete_subject(subject_id):
    subject = subject_controller.get_subject_by_id(subject_id)
    if subject_controller.check_if_user_owns_subject(subject.id, current_user.id):
        db.session.delete(subject)
        db.session.commit()
    return redirect(url_for("subjects.all_subjects"))
