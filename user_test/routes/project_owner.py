import flask
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import models
from google.appengine.ext import ndb
from models import ProjectUsers
from models import Team
from models import User
from models import STATUS_USER_PROJECT_APPLIED
from models import STATUS_USER_PROJECT_APPROVED
from models import STATUS_USER_PROJECT_DENIED
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
    participants_applied = []
    participants_approved = []
    participants_denied = []
    for project_user in project_users:
        participants.append(project_user.user.get())
        participants_applied.append(project_user.user.get())
        if project_user.status == STATUS_USER_PROJECT_APPROVED:
            participants_approved.append(project_user.user.get())
        elif project_user.status == STATUS_USER_PROJECT_DENIED:
            participants_denied.append(project_user.user.get())

    return render_template(
        'project_owner.html',
        project_details=project_details,
        participants=participants,
        participants_applied=participants_applied,
        participants_approved=participants_approved,
        participants_denied=participants_denied,
        team=team,
        user_photo_url=session['photo_url'],
        project_id=project_id,
    )


def get_user_project_entity(project_id, userid):
    project_details = ndb.Key('Project', project_id).get()

    current_user_project_record = ProjectUsers.query(
        ProjectUsers.project == ndb.Key('Project', int(project_id)),
        ProjectUsers.user == ndb.Key('User', int(userid)),
    ).get()

    return current_user_project_record



@project_owner.route('/project_owner/<int:project_id>/approve_user/<int:userid>', methods=['POST'])
@login_required
def approve_user_to_project(project_id, userid):
    current_user_project_record = get_user_project_entity(project_id, userid)
    current_user_project_record.status = STATUS_USER_PROJECT_APPROVED
    current_user_project_record.put()
    return redirect(flask.url_for('project_owner.main', project_id=project_id))


@project_owner.route('/project_owner/<int:project_id>/deny_user/<int:userid>', methods=['POST'])
@login_required
def deny_user_to_project(project_id, userid):
    current_user_project_record = get_user_project_entity(project_id, userid)
    current_user_project_record.status = STATUS_USER_PROJECT_DENIED
    current_user_project_record.put()
    return redirect(flask.url_for('project_owner.main', project_id=project_id))
