import flask
from flask import Blueprint, render_template, redirect
from gplus_oauth import CLIENT_SECRETS
from oauth2client import client


login = Blueprint('login', __name__, template_folder='templates')


@login.route('/login')
def login_page():
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.me',
        redirect_uri= flask.url_for('goog_auth_response.goog_auth_response_page', _external=True),
        login_hint='yelp.com',
    )
    return redirect(flow.step1_get_authorize_url())
