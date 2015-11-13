from flask import Blueprint
from flask import render_template
from flask import request
import models
from google.appengine.ext import ndb

project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project/<int:project_id>')
def main(project_id):
    project_details = ndb.Key('Project', project_id).get()
    return render_template('project.html', project_details=project_details)
