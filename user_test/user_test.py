import os
import sys

import random
import string

from flask import Flask

from routes.main import main
from routes.project import project
from routes.project_owner import project_owner
from routes.projects import projects
from routes.login import login
from routes.logout import logout
from routes.create_fake_project import create_fake_project
from routes.goog_auth_response import goog_auth_response
import upload


sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
app.register_blueprint(main)
app.register_blueprint(create_fake_project)
app.register_blueprint(project)
app.register_blueprint(project_owner)
app.register_blueprint(projects)
app.register_blueprint(goog_auth_response)
app.register_blueprint(login)
app.register_blueprint(logout)

# upload.run()
# upload.add_project()

app.debug = True
