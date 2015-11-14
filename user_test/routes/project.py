from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import models
from models import User
from models import Team
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

    return render_template(
        'project.html',
        project_details=project_details,
        project_id=project_id,
        user_photo_url=session['photo_url'],
        participants=[User(first_name="Kent", last_name="Wills", team=Team.query(Team.type == 'Yelp Consumer').get().key)]
    )

@project.route('/project/<int:project_id>/participate', methods=['GET'])
@login_required
def participate(project_id):
    project_users = ProjectUsers.query(ProjectUsers.project==ndb.Key(models.Project, project_id),
            ProjectUsers.status==models.STATUS_ACTIVE).fetch()
    print project_users
    current_user_id = session['user_id']
    project_record = None

    for record in project_users:
        if record.user.id() == current_user_id:
            project_record = record
            break
    
    if project_record is None:
        # User is not already participating, add that record to the database
        ProjectUsers(user=ndb.Key(models.User, current_user_id),
                project=ndb.Key(models.Project, project_id), status=models.STATUS_ACTIVE).put()
    else:
        # User is participating, issue a delete.
        models.ProjectUsers(user=current_user.key.id(),
                project=project_id, status=models.STATUS_DEACTIVE).put()

    return redirect('/project/' + str(project_id))
