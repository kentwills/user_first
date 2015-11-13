from flask import Blueprint, render_template, abort
import models

project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project')
def main():
    projects = models.Project.query()
    return render_template('project.html', team_list=projects)
