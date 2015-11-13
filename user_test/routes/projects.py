from flask import Blueprint, render_template, abort
import models

projects = Blueprint('projects', __name__, template_folder='templates')


@projects.route('/projects')
def main():
    project_list = models.Project.query()
    team_list = models.Team.query()
    return render_template('projects.html', project_list=project_list, team_list=team_list)
