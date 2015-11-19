from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
import models
from models import ProjectUsers
from google.appengine.ext import ndb
from route_utils import login_required

project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project/<int:project_id>')
@login_required
def main(project_id):
    project_details = ndb.Key('Project', project_id).get()
    # If the user is the owner of this event, then redirect to the owner page.

    if session['user_id'] == project_details.owner.id():
        return redirect('/project_owner/' + str(project_id))

    userid = session['user_id']
    current_user_project_record = ProjectUsers.query(
        ProjectUsers.project == ndb.Key('Project', project_id),
        ProjectUsers.user == ndb.Key('User', userid)
    ).get()

    project_users = models.ProjectUsers.query(
        models.ProjectUsers.project == ndb.Key('Project', project_id)
    ).fetch()

    participants = []
    for project_user in project_users:
        participants.append(project_user.user.get())

    return render_template(
        'project.html',
        project_details=project_details,
        project_id=project_id,
        user_photo_url=session['photo_url'],
        participants=participants,
        current_user_project_record=current_user_project_record
    )


@project.route('/project/<int:project_id>/participate', methods=['POST'])
@login_required
def participate(project_id):

    userid = session['user_id']
    current_user_project_record = ProjectUsers.query(
        ProjectUsers.project == ndb.Key('Project', project_id),
        ProjectUsers.user == ndb.Key('User', userid)
    ).get()

    if current_user_project_record is None:
        # User is not already participating, add that record to the database
        ProjectUsers(
            user=ndb.Key(models.User, userid),
            project=ndb.Key(models.Project, project_id),
            status=models.STATUS_USER_PROJECT_APPLIED
        ).put()
    else:
        # User is participating, issue a delete.
        current_user_project_record.key.delete()

    return redirect('/project/' + str(project_id))
