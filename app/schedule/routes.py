from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import and_
from app.extensions.database.models import Lesson, Subject, UserInSubject
from app.extensions.database.database import db
from app.helpers.helpers import Helpers

blueprint = Blueprint("schedule", __name__)

helpers = Helpers()


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
    given_date = helpers.make_string_into_date(date_string)

    week_days_list = helpers.make_a_list_of_week_days(given_date)
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

    list_of_schedule_times = helpers.make_a_list_of_hours(
        min_time_of_schedule, max_time_of_schedule
    )

    return render_template(
        "schedule/schedule.html",
        weekdates=week_days_list,
        times=list_of_schedule_times,
        lessons=all_lessons_list,
    )
