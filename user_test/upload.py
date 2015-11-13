import models


def run():
    add_teams()
    add_attributes()


def add_teams():
    models.Team(type='Eat24').put()
    models.Team(type='SeatMe').put()
    models.Team(type='Yelp-Biz').put()
    models.Team(type='Yelp-Consumer').put()


def add_attributes():
    models.Attribute(name='Age').put()
    models.Attribute(name='Sex').put()
