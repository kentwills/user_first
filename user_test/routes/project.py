from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
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
    user = ndb.Key('Users', project_details.owner.id()).get()
    # If the user is the owner of this event, then redirect to the owner page.
    if session['gplus_id'] == user.gplus_id:
        return redirect('/project_owner/project_id')


    
    return render_template(
        'project.html',
        project_details=project_details,
        attributes={"age": "31", "sex": "male"},
        user_photo_url=session['photo_url'],
        participants=[User(first_name="Kent", last_name="Wills", team=Team.query(Team.type == 'Yelp Consumer').get().key)]
    )

@project.route('/project/<int:project_id>/participate', METHODS=['POST'])
@login_required
def participate(project_id):
    current_user = User(gplus_id=session['gplus_id']).get()
    project_query = ProjectUsers(user=current_user.key.id(), project=project_id)
    project_record = project_query.get()

    project_users = ProjectUsers(project=project_id).fetch()
    for record in project_users:
        



    if project_record is None:
        # User is not already participating, add that record to the database
        ProjectUsers(user=current_user.key.id(),
                project=project_id, status=model.STATUS_ACTIVE).put()
    else:
        # User is participating, issue a delete.
        ProjectUsers(user=current_user.key.id(),
                project=project_id, status=model.STATUS_DEACTIVE).put()

    return redirect('/project/' + str(project_id))
