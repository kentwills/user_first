import os
import sys

from flask import Flask

from routes.sign import sign
from routes.main import main
from routes.project import project
from routes.login import login
from routes.goog_auth_response import goog_auth_response
#from gplus_oauth import oauth2_decorator

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))


app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(sign)
app.register_blueprint(project)
app.register_blueprint(goog_auth_response)
app.register_blueprint(login)

app.debug = True

@app.route('/projects')
def projects():
    #replace index.html with projects.html
    return render_template('index.html')
