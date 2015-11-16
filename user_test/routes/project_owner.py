from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
import models
from google.appengine.ext import ndb
from models import User
from models import Team
from route_utils import login_required

project_owner = Blueprint('project_owner', __name__, template_folder='templates')


@project_owner.route('/project_owner/<int:project_id>')
@login_required
def main(project_id):
    project_details = ndb.Key('Project', project_id).get()
    team = ndb.Key('Team', int(project_details.team.id())).get()

    project_users = models.ProjectUsers.query(
        models.ProjectUsers.project == ndb.Key('Project', project_id)
    ).fetch()

    participants = []
    for project_user in project_users:
        participants.append(project_user.user.get())

    return render_template(
        'project_owner.html',
        project_details=project_details,
        participants=participants,
        team=team,
        user_photo_url=session['photo_url'],
        project_id=project_id,
    )
