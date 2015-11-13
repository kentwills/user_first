from flask import Blueprint
from flask import redirect
from flask import session
from google.appengine.ext import ndb

from models import STATUS_DEACTIVE
from route_utils import login_required


deactivate_project = Blueprint('deactivate_project', __name__, template_folder='templates')


@deactivate_project.route('/deactivate_project/<int:project_id>', methods=["GET", "POST"])
@login_required
def deactivate_project_route(project_id):
    project_details = ndb.Key('Project', project_id).get()

    if session['user_id'] == project_details.owner.id():
        # Deactivate then redirect.
        project_details.status = STATUS_DEACTIVE
        project_details.put()
        return redirect('/project_owner/' + str(project_id))

    # If not owner of project, redirect to project page.
    return redirect('/project/' + str(project_id))


