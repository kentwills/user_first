
import urllib

from flask import request
from models import Author
from models import Greeting
from flask import redirect
from google.appengine.api import users
from google.appengine.ext import ndb

from gplus_oauth import flow
#from gplus_oauth import service

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


from flask import Blueprint, render_template, abort, redirect
from gplus_oauth import flow

main = Blueprint('main', __name__, template_folder='templates')

#@oauth2_decorator.oauth_required
@main.route('/')
def main_page():
    #return redirect(flow.step1_get_authorize_url())
    return render_template('welcome.html', auth_url=flow.step1_get_authorize_url())


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)
