from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request

from gplus_oauth import flow


goog_auth_response = Blueprint('goog_auth_response', __name__, template_folder='templates')


@goog_auth_response.route('/oauth2callback')
def goog_auth_response_page():
    error = request.args.get('error', '')
    auth_code  = request.args.get('code', '')

    if error:
        # uh oh
        return error
    elif auth_code:
        # yay
        credentials = flow.step2_exchange(auth_code)
        return str(auth_code)


# https://oauth2-login-demo.appspot.com/auth?error=access_denied
# https://oauth2-login-demo.appspot.com/auth?code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7
