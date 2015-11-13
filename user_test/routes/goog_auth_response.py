import httplib2
import json

import flask
from flask import Blueprint
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from googleapiclient import discovery
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
        http_auth = credentials.authorize(httplib2.Http())
        plus_service = discovery.build('plus', 'v1', http=http_auth)
        goog_request = plus_service.people().get(userId='me')
        result = goog_request.execute(http=http_auth)

        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
        #return str(user_info.name.formatted_name)


# https://oauth2-login-demo.appspot.com/auth?error=access_denied
# https://oauth2-login-demo.appspot.com/auth?code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7
