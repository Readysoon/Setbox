from flask import Blueprint, render_template, redirect, url_for, request
from app import app

blueprint = Blueprint('subjects', __name__)

@blueprint.route('/')
@blueprint.route('/subject')
def subjects():
    connection = app.get_database_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT subjects.id, subjects.name FROM users JOIN subjects ON users.id = subjects.owner_user_id WHERE '
        'users.id = 1')
    subject_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('subjects/subjects_page.html', subject_names=subject_names)


@blueprint.route('/subject/<subject_id>')
def subject(subject_id):
    connection = app.get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT subjects.name FROM subjects WHERE subjects.id = ' + subject_id)
    subject_name = cursor.fetchone()
    cursor.execute(
        "SELECT TO_CHAR(lesson.date, 'dd.mm.yyyy'), lesson.name, lesson.progress, lesson.id FROM subjects " +
        "JOIN lesson ON subjects.id = lesson.subject_id WHERE subjects.id = " + subject_id +
        " ORDER BY lesson.date DESC")
    subject_info = cursor.fetchall()
    cursor.execute('SELECT lesson.progress FROM lesson WHERE lesson.subject_id =' + subject_id)
    all_progress = cursor.fetchall()
    progress = 0
    divide = 0
    for each_progress in all_progress:
        if each_progress[0] is not None:
            progress = progress + int(each_progress[0])
        divide = divide + 1
    progress = progress / divide
    cursor.close()
    connection.close()
    return render_template('subjects/subject.html', subject_name=subject_name, subject_info=subject_info, progress=progress)

