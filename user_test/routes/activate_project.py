from flask import Blueprint
from flask import redirect
from flask import session
from google.appengine.ext import ndb

from models import STATUS_ACTIVE
from route_utils import login_required


activate_project = Blueprint('activate_project', __name__, template_folder='templates')


@activate_project.route('/activate_project/<int:project_id>', methods=["GET", "POST"])
@login_required
def activate_project_route(project_id):
    project_details = ndb.Key('Project', project_id).get()

    if session['user_id'] == project_details.owner.id():
        # activate then redirect.
        project_details.status = STATUS_ACTIVE
        project_details.put()
        return redirect('/project_owner/' + str(project_id))

    # If not owner of project, redirect to project page.
    return redirect('/project/' + str(project_id))


