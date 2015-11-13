from flask import Blueprint, render_template, redirect

from gplus_oauth import flow


welcome = Blueprint('welcome', __name__, template_folder='templates')


@welcome.route('/login')
def welcome_page():
    return redirect(flow.step1_get_authorize_url())
    #return render_template('welcome.html')
