from google.appengine.ext import ndb


class Attribute(ndb.Model):
    name = ndb.StringProperty()


class User(ndb.Model):
    """Model for our Users"""
    token = ndb.IntegerProperty()
    admin = ndb.IntegerProperty()
    attributes = ndb.KeyProperty(kind="Attributes")


class Project(ndb.Model):
    """PM projects"""
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


class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)