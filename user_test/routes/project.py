from flask import Blueprint, render_template, abort
import models

project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project')
def main():
    project_details = models.Project.query()
    return render_template('project.html', project_details=project_details)
