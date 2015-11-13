from flask import Blueprint, render_template, abort
import models

project = Blueprint('project', __name__, template_folder='templates')


@project.route('/project')
def main():
    teams = models.Team.query()
    return render_template('logged_in.html', team_list=teams)
