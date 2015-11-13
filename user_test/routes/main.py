import flask
from gplus_oauth import CLIENT_SECRETS
from oauth2client import client

from flask import Blueprint, render_template


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def main_page():
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.me',
        redirect_uri = flask.url_for('goog_auth_response.goog_auth_response_page', _external=True),
    )
    return render_template('welcome.html', auth_url=flow.step1_get_authorize_url())
