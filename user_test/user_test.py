import os
import sys

import httplib2
import jinja2
from flask import Flask
from flask import render_template
from routes.sign import sign
from routes.main import main
from routes.project import project
from routes.welcome import welcome
from routes.goog_auth_response import goog_auth_response
from gplus_oauth import oauth2_decorator

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))


app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(sign)
app.register_blueprint(project)
app.register_blueprint(goog_auth_response)

app.debug = True

@app.route('/projects')
def projects():
    #replace index.html with projects.html
    return render_template('index.html')

@app.route(oauth2_decorator.callback_path)
def authorize_user():
    return request.query_string
#    return oauth2_decorator.callback_handler()
