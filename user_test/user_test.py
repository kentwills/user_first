import os
import sys

import httplib2
import jinja2
from flask import Flask
from routes.sign import sign
from routes.main import main
#from routes.project import project

from googleapiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache


sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))


app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(sign)
#app.register_blueprint(project)

app.debug = True

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

http = httplib2.Http(memcache)

service = discovery.build("plus", "v1", http=http)

"""
oauth2_decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    message=MISSING_CLIENT_SECRETS_MESSAGE,
)

@app.route(oauth2_decorator.callback_path)
def authorize_user():
    return oauth2_decorator.callback_handler()
"""