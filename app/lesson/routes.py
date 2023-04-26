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
import filetype
from app.subjects.controllers import SubjectController
from app.lesson.controllers import LessonController

blueprint = Blueprint("lesson", __name__)
lesson_controller = LessonController()
subject_controller = SubjectController()


@blueprint.get("/lesson/<lesson_id>")
@login_required
def lesson_page(lesson_id):
    return render_template(
        "lesson/lesson.html",
        lesson=lesson_controller.get_lesson_and_subject_by_lesson_id(lesson_id),
        files=lesson_controller.get_files_in_lesson(lesson_id),
    )


@blueprint.post("/lesson/<lesson_id>")
@login_required
def change_lesson_name(lesson_id):
    lesson_controller.change_lesson_name(lesson_id, request.form.get("lessonname"))
    return redirect(url_for("lesson.lesson_page", lesson_id=lesson_id))


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
    lesson_controller.add_file_to_db(name, lesson_id, filename, file_type)
    return redirect(url_for("lesson.lesson_page", lesson_id=lesson_id))


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
    lesson_id = lesson_controller.get_lesson_id_from_file_id(file_id)
    lesson_controller.delete_file(file_id)
    return redirect(url_for("lesson.lesson_page", lesson_id=lesson_id))


@blueprint.route("/done/<file_id>")
@login_required
def done(file_id):
    lesson_id = lesson_controller.get_file_by_file_id(file_id).lesson_id
    lesson_controller.change_file_to_done(file_id)
    return redirect(url_for("lesson.lesson_page", lesson_id=lesson_id))


@blueprint.route("/files/<filename>", methods=["GET"])
@login_required
def download(filename):
    file_path = "../files/" + filename
    return make_response(send_file(file_path))


@blueprint.get("/lessonadder")
@login_required
def addlesson():
    return render_template(
        "lesson/lessonadder.html",
        subjects=subject_controller.find_all_subjects_owned_or_editor(current_user.id),
    )


@blueprint.post("/lessonadder")
@login_required
def addlesson_post():
    name = request.form["lesson_name"]
    subject_id = request.form["subjects"]
    date = request.form["lesson_date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    if subject_controller.check_if_user_is_owner_or_editor(subject_id, current_user.id):
        lesson = lesson_controller.create_lesson(
            subject_id, date, start_time, end_time, name
        )
    return redirect(url_for("lesson.lesson_page", lesson_id=lesson.id))


@blueprint.post("/delete_lesson/<lesson_id>")
@login_required
def delete_lesson(lesson_id):
    lesson = lesson_controller.get_lesson_by_lesson_id(lesson_id)
    subject_id = lesson.subject_id
    lesson_controller.delete_lesson(lesson)
    return redirect(url_for("subjects.subject_page", subject_id=subject_id))
