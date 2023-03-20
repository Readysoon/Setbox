from flask import Blueprint, render_template

blueprint = Blueprint('schedule', __name__)

@blueprint.route('/schedule')
def schedule():
    return render_template('schedule/schedule.html')