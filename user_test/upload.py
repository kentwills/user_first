import models
from google.appengine.ext import ndb


def run():
    delete_all()
    add_teams()
    add_attributes()
    add_project()


def add_teams():
    models.Team(type='Eat24').put()
    models.Team(type='SeatMe').put()
    models.Team(type='Yelp Biz').put()
    models.Team(type='Yelp Consumer').put()


def add_attributes():
    models.Attribute(name='Age').put()
    models.Attribute(name='Sex').put()


def add_project():

    models.User(token=12342341, admin=1, first_name='Kent', last_name='Wills').put()
    team = models.Team.query().get().key
    user = models.User.query().get().key

    models.Project(
        owner=user,
        team=team,
        title='Test the full user flow',
        description='We will spend 30 minutes to test the user flows for the eat24 app.',
        location='13F CarPort',
        status=True
    ).put()


def delete_all():
    ndb.delete_multi(models.Project.query().fetch(keys_only=True))
    ndb.delete_multi(models.Team.query().fetch(keys_only=True))
    ndb.delete_multi(models.ProjectUsers.query().fetch(keys_only=True))
