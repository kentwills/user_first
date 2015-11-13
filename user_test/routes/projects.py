import models
import pprint
import datetime

from flask import Blueprint, render_template, abort
from flask import request
from flask import redirect


projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/projects', methods=["GET", "POST"])
def main():

    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['description']
        location = request.form['location']
        room_name = request.form['room_name']
        product_type = request.form['product_type']
        time = request.form['time_frame']
        date = request.form['date']
        qualifications = request.form['qualifications']

        models.Project(
                owner=models.User.query().get().key,
                team=models.Team.query().get().key,
                title=project_name,
                description=project_description,
                date_time=datetime.datetime.strptime(date, '%m/%d/%Y'),
                time_range=time,
                location=location,
                room_name=room_name,
                status=models.STATUS_ACTIVE,
                qualifications=qualifications
                ).put()
        return redirect('/project_owner/' + str(project.id()))
    else:
        project_list = models.Project.query()
        team_list = models.Team.query()
        return render_template('projects.html', project_list=project_list, team_list=team_list)

