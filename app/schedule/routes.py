from datetime import datetime, timedelta, time
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import and_
from app.extensions.database.models import Lesson, Subject, UserInSubject
from app.extensions.database.database import db

blueprint = Blueprint("schedule", __name__)


@blueprint.get("/schedule/")
@blueprint.get("/schedule")
@login_required
def schedule_no_date():
    return redirect(
        url_for(
            "schedule.create_schedule", date_string=datetime.now().strftime("%Y-%m-%d")
        )
    )


@blueprint.post("/schedule")
@login_required
def schedule_post_date():
    date = request.form.get("date")
    return redirect(url_for("schedule.create_schedule", date_string=date))


@blueprint.route("/schedule/<date_string>")
@login_required
def create_schedule(date_string):
    # lists that will be used for storing data
    all_lessons_list = []

    given_date = datetime.strptime(date_string, "%Y-%m-%d")

    week_days_list = make_a_list_of_week_days(given_date)
    first_day_of_week = datetime.strptime(week_days_list[0], "%d.%m.%Y")
    last_day_of_week = datetime.strptime(week_days_list[6], "%d.%m.%Y")

    all_lessons_list = (
        db.session.query(Lesson, Subject)
        .filter(
            and_(Lesson.date >= first_day_of_week), (Lesson.date <= last_day_of_week)
        )
        .join(Subject)
        .join(UserInSubject, isouter=True)
        .filter(
            (Subject.owner_user_id == current_user.id)
            | (UserInSubject.user_id == current_user.id)
        )
        .order_by(Lesson.start_time)
        .all()
    )

    if all_lessons_list == []:
        return render_template(
            "schedule/schedule.html", weekdates=week_days_list, times=[], lessons=[]
        )

    min_time_of_schedule = all_lessons_list[0].Lesson.start_time
    max_time_of_schedule = all_lessons_list[-1].Lesson.end_time

    list_of_schedule_times = make_a_list_of_hours(
        min_time_of_schedule, max_time_of_schedule
    )

    return render_template(
        "schedule/schedule.html",
        weekdates=week_days_list,
        times=list_of_schedule_times,
        lessons=all_lessons_list,
    )


def make_a_list_of_week_days(date):
    given_day_of_week = date.strftime("%w")
    if int(given_day_of_week) == 0:
        given_day_of_week = 7
    week_dates = []
    for day_of_week in range(1, 8):
        day = date + timedelta(days=-int(given_day_of_week) + day_of_week)
        day_string = day.strftime("%d.%m.%Y")
        week_dates.append(day_string)
    return week_dates


def round_time(given_time):
    return given_time.replace(minute=0, second=0, microsecond=0)


def round_time_to_next_hour(given_time):
    if given_time.replace(hour=0) > time(minute=0):
        return round_time(given_time).replace(hour=given_time.hour + 1)
    return round_time(given_time)


def make_a_list_of_hours(start_time, end_time):
    list_of_hours = []
    start_time_rounded = round_time(start_time)
    end_time_rounded = round_time_to_next_hour(end_time)
    hour_in_list = start_time_rounded
    while hour_in_list <= end_time_rounded:
        list_of_hours.append(hour_in_list)
        hour_in_list = hour_in_list.replace(hour=hour_in_list.hour + 1)
    return list_of_hours
