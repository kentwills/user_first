"""
Logout route.
"""
import flask
from flask import Blueprint
from flask import redirect
from flask import session

logout = Blueprint('logout', __name__, template_folder='templates')


@logout.route('/logout')
def logout_route():
    session['gplus_access_token'] = None
    session['gplus_id'] = None
    session['goog_auth_expire_time'] = None
    session['photo_url'] = None

    return redirect(flask.url_for('main.main_page'))
