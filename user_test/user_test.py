import os
import sys

from flask import Flask

from routes.main import main
from routes.project import project
from routes.project_owner import project_owner
from routes.projects import projects
from routes.login import login
from routes.create_fake_project import create_fake_project
from routes.goog_auth_response import goog_auth_response
import upload


sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(create_fake_project)
app.register_blueprint(project)
app.register_blueprint(project_owner)
app.register_blueprint(projects)
app.register_blueprint(goog_auth_response)
app.register_blueprint(login)

#upload.run()
#upload.add_project()

app.debug = True
