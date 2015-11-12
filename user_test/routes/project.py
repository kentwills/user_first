import urllib

from flask import request
from models import Author
from models import Greeting
from flask import redirect
from google.appengine.api import users
from google.appengine.ext import ndb


from flask import Blueprint, render_template, abort

project = Blueprint('project', __name__,
                 template_folder='templates')

@project.route('/project')
def project():
    return render_template('old_index.html')
