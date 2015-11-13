from flask import Blueprint, render_template, abort
from flask import request
import models
import pprint

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/projects', methods=["GET", "POST"])
def main():
    if request.method == 'GET': 
        project_list = models.Project.query()
        team_list = models.Team.query()
        return render_template('projects.html', project_list=project_list, team_list=team_list)
    else:
        project_name = request.form['project_name']
        project_description = request.form['description']
        location = request.form['location']
        room_name = request.form['room_name']
        product_type = request.form['product_type']
        time = request.form['time_frame']
        date = request.form['date']
        qualifications = request.form['qualifications']

        return pprint.pformat(request.form) 
