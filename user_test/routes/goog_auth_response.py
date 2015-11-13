import httplib2
import json

import flask
from flask import Blueprint
from flask import request
from flask import make_response
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
        return str(error)
    elif auth_code:
        # creds' Class: oauth2client.client.OAuth2Credentials
        credentials = flow.step2_exchange(auth_code)
        http_auth = credentials.authorize(httplib2.Http())
        plus_service = discovery.build('plus', 'v1', http=http_auth)
        goog_request = plus_service.people().get(userId='me')
        result = goog_request.execute(http=http_auth)
        result['creds'] = credentials.to_json()

        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
        #return str(user_info.name.formatted_name)

# https://oauth2-login-demo.appspot.com/auth?error=access_denied
# https://oauth2-login-demo.appspot.com/auth?code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7


# 834 char id_token

# Credentials .to_json() looks like:
"""
{
    "token_response": {
        "token_type": "Bearer",
        "expires_in": 3598,
        "access_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "id_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    },
    "_module": "oauth2client.client",
    "client_id": "999999999999-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com",
    "revoke_uri": "https:g/accounts.google.com/o/oauth2/revoke",
    "scopes": ["https://www.googleapis.com/auth/plus.me"],
    "invalid": False,
    "token_info_uri": "https://www.googleapis.com/oauth2/v2/tokeninfo",
    "client_secret": "XXXXXXXXXXXXXXXXXXXXXXXX",
    "refresh_token": None,
    "id_token": {
        "sub": "999999999999999999999",
        "iss": "accounts.google.com",
        "at_hash": "XXXXXXXXXXXXXXXXXXXXXX",
        "aud": "999999999999-xxxxxxxxxxxx9xx9xx9xxxxxxxxxxxxx.apps.googleusercontent.com",
        "iat": 9999999999,
        "azp": "999999999999-xxxxxxxxxxxx9xx9xx9xxxxxxxxxxxxx.apps.googleusercontent.com",
        "exp": 9999999999
    },
    "_class": "OAuth2Credentials",
    "user_agent": null,
    "access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "token_expiry": "2015-11-13T06:25:12Z"
}
"""