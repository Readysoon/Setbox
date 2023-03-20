import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

def get_database_connection():
    connection = psycopg2.connect(
        host = "localhost",
        database = "setbox",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return connection

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/subject')
def subjects():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT subjects.id, subjects.name FROM users JOIN subjects ON users.id = subjects.owner_user_id WHERE users.id = 1')
    subject_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('subjects_page.html', subject_names=subject_names)

@app.route('/subject/<subject_id>')
def subject(subject_id):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT subjects.name FROM subjects WHERE subjects.id = ' + subject_id)
    subject_name = cursor.fetchone()
    cursor.execute("SELECT TO_CHAR(lesson.date, 'dd.mm.yyyy'), lesson.name, lesson.progress, lesson.id FROM subjects JOIN lesson ON subjects.id = lesson.subject_id WHERE subjects.id = " + subject_id + " ORDER BY lesson.date DESC")
    subject_info = cursor.fetchall()
    cursor.execute('SELECT lesson.progress FROM lesson WHERE lesson.subject_id =' + subject_id)
    all_progress = cursor.fetchall()
    progress = 0
    divide = 0
    for each_progress in all_progress:
        if each_progress[0] != None:
            progress = progress + int(each_progress[0])
        divide = divide + 1
    progress = progress / divide
    cursor.close()
    connection.close()
    return render_template('subject.html', subject_name = subject_name, subject_info=subject_info, progress = progress)

@app.route('/lesson/<lesson_id>')
def lesson(lesson_id):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT subjects.name, lesson.name, TO_CHAR(lesson.date, 'dd.mm.yyyy') FROM subjects JOIN lesson ON subjects.id = lesson.subject_id WHERE lesson.id = " + lesson_id)
    lesson_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('lesson.html', info=lesson_info)
