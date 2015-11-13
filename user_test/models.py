from google.appengine.ext import ndb


class ProjectAttribute(ndb.Model):
    project = ndb.KeyProperty(kind="Project")
    attribute = ndb.KeyProperty(kind="Attribute")


class UserAttribute(ndb.Model):
    user = ndb.KeyProperty(kind="User")
    attribute = ndb.KeyProperty(kind="Attribute")


class Attribute(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()


class User(ndb.Model):
    token = ndb.IntegerProperty()
    admin = ndb.IntegerProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()


class Project(ndb.Model):
    owner = ndb.KeyProperty(kind="User")
    team = ndb.KeyProperty(kind="Team")
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    date_time = ndb.DateTimeProperty()
    location = ndb.StringProperty()
    status = ndb.IntegerProperty()


class ProjectUsers(ndb.Model):
    project = ndb.KeyProperty(kind="Project")
    user = ndb.KeyProperty(kind="User")
    status = ndb.IntegerProperty()


class Team(ndb.Model):
    type = ndb.StringProperty()
