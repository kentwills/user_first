import httplib2
import json
import time
from datetime import datetime
from datetime import timedelta

import flask
from flask import Blueprint
from flask import redirect
from flask import request
from flask import make_response
from flask import session
from googleapiclient import discovery
from gplus_oauth import CLIENT_SECRETS
from oauth2client import client

from models import Team
from models import User


goog_auth_response = Blueprint('goog_auth_response', __name__, template_folder='templates')


@goog_auth_response.route('/oauth2callback')
def goog_auth_response_page():
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope=['https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri= flask.url_for('goog_auth_response.goog_auth_response_page', _external=True),
        login_hint='yelp.com',
    )

    error = request.args.get('error', '')
    auth_code  = request.args.get('code', '')

    if error:
        return str(error)
    elif auth_code:
        # creds' Class: oauth2client.client.OAuth2Credentials
        credentials = flow.step2_exchange(auth_code)

        # Get User Info from GPlus.
        http_auth = credentials.authorize(httplib2.Http())
        plus_service = discovery.build('plus', 'v1', http=http_auth)
        goog_request = plus_service.people().get(userId='me')
        result = goog_request.execute(http=http_auth)
        result['creds'] = credentials.to_json()

        # Check if we have user, or make new user.
        gplus_id = int(credentials.id_token['sub'])
        gplus_email = str(credentials.id_token['email'])

        if gplus_email.find('@yelp.com') == -1:
            return "You must use a @yelp.com email."

        seconds_til_expire = credentials.token_response['expires_in']
        current_time = time.mktime(datetime.now().timetuple())
        expire_time = current_time + seconds_til_expire

        stored_access_token = session.get('gplus_access_token')
        stored_gplus_id = session.get('gplus_id')
        stored_expire_time = session.get('goog_auth_expire_time')

        # Update session info with newest expire time/creds.
        session['gplus_access_token'] = credentials.access_token
        session['gplus_id'] = gplus_id
        session['goog_auth_expire_time'] = expire_time
        session['photo_url'] = result['image']['url']

        if (
                stored_access_token is not None and
                gplus_id == stored_gplus_id and
                stored_expire_time and
                current_time < stored_expire_time
        ):
            # User was connected, redirect to projects (or fill-in-user info?)
            return redirect(flask.url_for('projects.main'))
        else:
            # If user doesn't exist, make new user.
            stored_user = User.query(User.gplus_id == str(gplus_id)).get()
            if stored_user is None:
                # Create a new user.
                new_user = User(
                    gplus_id=str(gplus_id),
                    gplus_email=gplus_email,
                    admin=1,
                    first_name=result['name']['givenName'],
                    last_name=result['name']['familyName'],
                    photo_url=result['image']['url'],
                    team=Team.query(Team.type == 'Yelp Consumer').get().key
                )
                new_user_key = new_user.put()
                session["user_id"] = new_user_key.id()
                # REDIR to fill_out_your_info or project page?
                return redirect(flask.url_for('projects.main'))
            else:
                session["user_id"] = stored_user.key.id()
                # User exists! Show project page (or fill_out_info if missing info?).
                return redirect(flask.url_for('projects.main'))

        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

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
