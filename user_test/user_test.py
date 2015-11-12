import cgi
import os
import sys
import urllib

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

from flask import request
from flask import Flask
from flask import render_template
from flask import redirect
from google.appengine.api import users
from google.appengine.ext import ndb
import models

import jinja2

from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
app = Flask(__name__)
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

#http = httplib2.Http(memcache)
#service = discovery.build("plus", "v1", http=http)
#decorator = appengine.oauth2decorator_from_clientsecrets(
#    CLIENT_SECRETS,
#    scope='https://www.googleapis.com/auth/plus.me',
#    message=MISSING_CLIENT_SECRETS_MESSAGE)
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

@app_route('/projects')
def projects():
    #replace index.html with projects.html
    return render_template('index.html')


@app.route('/')
def main_page():
    """
    @decorator.oauth_required
    def get(self):
    try:
      http = decorator.http()
      user = service.people().get(userId='me').execute(http=http)
      text = 'Hello, %s!' % user['displayName']

      template = JINJA_ENVIRONMENT.get_template('welcome.html')
      self.response.write(template.render({'text': text }))
    except client.AccessTokenRefreshError:
      self.redirect('/')
    """
    guestbook_name = request.args.get('guestbook_name',
                                      DEFAULT_GUESTBOOK_NAME)
    greetings_query = models.Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-models.Greeting.date)
    greetings = greetings_query.fetch(10)

    user = users.get_current_user()
    if user:
        url = users.create_logout_url(request.base_url)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.base_url)
        url_linktext = 'Login'

    return render_template('index.html', user=user, greetings=greetings,
            guestbook_name=urllib.quote_plus(guestbook_name), url=url,
            url_linktext=url_linktext)

"""class AboutHandler(webapp2.RequestHandler):

  #@decorator.oauth_required
  def get(self):
    try:
      http = decorator.http()
      user = service.people().get(userId='me').execute(http=http)
      text = 'Hello, %s!' % user['displayName']

      template = JINJA_ENVIRONMENT.get_template('welcome.html')
      self.response.write(template.render({'text': text }))
    except client.AccessTokenRefreshError:
      self.redirect('/')
"""
@app.route('/sign', methods=['POST'])
def guestbook():
    # We set the same parent key on the 'Greeting' to ensure each
    # Greeting is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second.
    guestbook_name = request.args.get('guestbook_name',
                                      DEFAULT_GUESTBOOK_NAME)
    greeting = models.Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
        greeting.author = models.Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

    greeting.content = request.form['content']
    greeting.put()

    query_params = {'guestbook_name': guestbook_name}
    return redirect('/?' + urllib.urlencode(query_params))
