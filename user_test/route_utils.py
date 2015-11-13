"""
Route utilities:
  - Wrapper to determine if user needs to login.
"""

import time
from functools import wraps
from datetime import datetime

#from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verify user is logged in with non-expired credentials.
        # If not, redirect to main page for login.

        current_time = time.mktime(datetime.now().timetuple())
        stored_access_token = session.get('gplus_access_token')
        stored_gplus_id = session.get('gplus_id')
        stored_expire_time = session.get('goog_auth_expire_time')

        if (
                stored_access_token is not None and
                stored_gplus_id is not None and
                stored_expire_time is not None and
                current_time < stored_expire_time
        ):
            # Everything checks out? Continue with original route.
            return f(*args, **kwargs)

        # Missing or expired creds:
        return redirect(url_for('main.main_page'))

    return decorated_function
