from flask import Blueprint, render_template
from app import app

blueprint = Blueprint('lesson', __name__)
@blueprint.route('/lesson/<lesson_id>')
def lesson(lesson_id):
    connection = app.get_database_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT subjects.name, lesson.name, TO_CHAR(lesson.date, 'dd.mm.yyyy'), subjects.id FROM subjects " +
        "JOIN lesson ON subjects.id = lesson.subject_id WHERE lesson.id = " + lesson_id)
    lesson_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('lesson/lesson.html', info=lesson_info)