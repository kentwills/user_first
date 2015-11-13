
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

    return render_template('welcome.html')


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)
