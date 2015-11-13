import flask
from flask import Blueprint
from flask import request
from gplus_oauth import CLIENT_SECRETS
from oauth2client import client


goog_auth_response = Blueprint('goog_auth_response', __name__, template_folder='templates')


@goog_auth_response.route('/oauth2callback')
def goog_auth_response_page():
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.me',
        redirect_uri= flask.url_for('goog_auth_response.goog_auth_response_page', _external=True),
    )

    error = request.args.get('error', '')
    auth_code  = request.args.get('code', '')

    if error:
        # uh oh
        return str(error)
    elif auth_code:
        # yay
        credentials = flow.step2_exchange(auth_code)
        return str(auth_code)

# https://oauth2-login-demo.appspot.com/auth?error=access_denied
# https://oauth2-login-demo.appspot.com/auth?code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7
