import os
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    make_response,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import and_, or_
import filetype
from app.extensions.database.database import db
from app.extensions.database.models import Subject, Lesson, File, User, UserInSubject

blueprint = Blueprint("lesson", __name__)


@blueprint.get("/lesson/<lesson_id>")
@login_required
def lesson_page(lesson_id):
    lesson = (
        db.session.query(Lesson, Subject)
        .filter(Subject.id == Lesson.subject_id)
        .filter(Lesson.id == lesson_id)
        .first()
    )
    files_in_lesson = (
        File.query.filter(File.lesson_id == Lesson.id)
        .filter(Lesson.id == lesson_id)
        .all()
    )
    return render_template("lesson/lesson.html", lesson=lesson, files=files_in_lesson)


@blueprint.post("/lesson/<lesson_id>")
@login_required
def change_lesson_name(lesson_id):
    lesson = Lesson.query.filter(Lesson.id == lesson_id).first()
    lesson.name = request.form.get("lessonname")
    db.session.commit()
    return redirect(url_for("lesson.lesson", lesson_id=lesson_id))


@blueprint.route("/upload/<lesson_id>", methods=["POST"])
@login_required
def upload(lesson_id):
    file = request.files["file"]
    name = request.form["name"]
    filename = (
        str(lesson_id)
        + "_"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + "_"
        + secure_filename(file.filename)
    )
    file.save("./files/" + filename)
    file_type = get_file_type(filename)
    file_to_db = File(filename=filename, name=name, lesson_id=lesson_id, type=file_type)
    db.session.add(file_to_db)
    db.session.commit()
    return redirect(url_for("lesson.lesson", lesson_id=lesson_id))


def get_file_type(filename):
    kind = filetype.guess("./files/" + filename)
    if kind is None:
        file_type = "Other"
    else:
        file_type = kind.mime
    return file_type


@blueprint.route("/delete/<file_id>")
@login_required
def delete(file_id):
    file = File.query.filter(File.id == file_id).first()
    lesson_id = file.lesson_id
    os.remove("./files/" + file.filename)
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for("lesson.lesson", lesson_id=lesson_id))


@blueprint.route("/done/<file_id>")
@login_required
def done(file_id):
    file = File.query.filter(File.id == file_id).first()
    file.reviewed = True
    db.session.commit()
    return redirect(url_for("lesson.lesson", lesson_id=file.lesson_id))


@blueprint.route("/files/<filename>", methods=["GET"])
@login_required
def download(filename):
    file_path = "../files/" + filename
    response = make_response(send_file(file_path))
    return response


@blueprint.get("/lessonadder")
@login_required
def addlesson():
    subjects = (
        Subject.query.join(UserInSubject)
        .filter(
            or_(
                Subject.owner_user_id == current_user.id,
                and_(
                    UserInSubject.user_id == current_user.id,
                    UserInSubject.editor is True,
                ),
            )
        )
        .all()
    )
    return render_template("lesson/lessonadder.html", subjects=subjects)


@blueprint.post("/lessonadder")
@login_required
def addlesson_post():
    name = request.form["lesson_name"]
    subject_id = request.form["subjects"]
    date = request.form["lesson_date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    lesson = Lesson(
        subject_id=subject_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        name=name,
    )
    subject = Subject.query.filter(Subject.id == subject_id).first()
    user_in_subject = (
        UserInSubject.query.filter(Subject.id == subject_id)
        .filter(User.id == current_user.id)
        .first()
    )
    if (
        subject.owner_user_id == current_user.id
        or user_in_subject is not None
        and user_in_subject.editor is True
    ):
        db.session.add(lesson)
        db.session.commit()
    return redirect(url_for("lesson.lesson", lesson_id=lesson.id))


@blueprint.post("/delete_lesson/<lesson_id>")
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.filter(Lesson.id == lesson_id).first()
    subject_id = lesson.subject_id
    db.session.delete(lesson)
    db.session.commit()
    return redirect(url_for("subjects.subject", subject_id=subject_id))
