from flask import Blueprint, render_template, abort
import upload

create_fake_project = Blueprint('create_fake_project', __name__, template_folder='templates')


@create_fake_project.route('/create_fake_project')
def main():
    upload.run()
    return render_template('success.html')
