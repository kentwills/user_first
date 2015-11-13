from flask import Blueprint, render_template, abort
import models
from datetime import date

create_fake_project = Blueprint('create_fake_project', __name__, template_folder='templates')


@create_fake_project.route('/create_fake_project')
def main():
    #models.User(token=12342341, admin=1, first_name='Kent', last_name='Wills').put()
    team = models.Team.query().get().key
    user = models.User.query().get().key

    """
    models.Project(
        owner=user,
        team=team,
        title='Test the full user flow',
        description='We will spend 30 minutes to test the user flows for the eat24 app.',
        date_time=date(),
        location='13F CarPort',
        status=True
    ).put()
    """
    p = models.Project.query().get()
    import pdb; pdb.set_trace()

    return render_template('success.html')
