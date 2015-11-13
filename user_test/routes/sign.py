import urllib

from flask import request
from models import Author
from models import Greeting
from flask import redirect
from google.appengine.api import users
from google.appengine.ext import ndb


from flask import Blueprint, render_template, abort

sign = Blueprint('sign', __name__,
                        template_folder='templates')


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


@sign.route('/sign', methods=['POST'])
def guestbook():
    # We set the same parent key on the 'Greeting' to ensure each
    # Greeting is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second.
    guestbook_name = request.args.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
        greeting.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

    greeting.content = request.form['content']
    greeting.put()

    query_params = {'guestbook_name': guestbook_name}
    return redirect('/?' + urllib.urlencode(query_params))


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

