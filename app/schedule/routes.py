from datetime import datetime
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from app.helpers.helpers import Helpers
from app.lesson.controllers import LessonController

blueprint = Blueprint("schedule", __name__)

helpers = Helpers()
lesson_controller = LessonController()


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

    all_lessons_list = lesson_controller.get_all_lessons_with_subjects_within_dates(
        first_day_of_week, last_day_of_week, current_user.id
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
