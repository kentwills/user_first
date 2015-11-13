from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
import models
from google.appengine.ext import ndb
from models import User
from models import Team

from route_utils import login_required


project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project/<int:project_id>')
@login_required
def main(project_id):
    project_details = ndb.Key('Project', project_id).get()

    return render_template(
        'project.html',
        project_details=project_details,
        user_photo_url=session['photo_url'],
        participants=[User(first_name="Kent", last_name="Wills", team=Team.query(Team.type == 'Yelp Consumer').get().key)]
    )
