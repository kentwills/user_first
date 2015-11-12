import os
import sys

from flask import Flask
import jinja2
from routes.sign import sign
from routes.main import main
#from routes.project import project


sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(sign)
#app.register_blueprint(project)

app.debug = True
