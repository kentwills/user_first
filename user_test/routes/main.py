
import urllib

from flask import request
from models import Author
from models import Greeting
from flask import redirect
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


from flask import Blueprint, render_template, abort

main = Blueprint('main', __name__,
                 template_folder='templates')
@main.route('/')
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
    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    user = users.get_current_user()
    if user:
        url = users.create_logout_url(request.base_url)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(request.base_url)
        url_linktext = 'Login'

    return render_template('old_index.html', user=user, greetings=greetings,
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


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)
