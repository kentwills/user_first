from google.appengine.ext import ndb

STATUS_ACTIVE = 1;
STATUS_DEACTIVE = 0;


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
    gplus_id = ndb.StringProperty()
    gplus_email = ndb.StringProperty()
    admin = ndb.IntegerProperty()  # 1=admin, 0=normal user.
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    photo_url = ndb.StringProperty()
    team = ndb.KeyProperty(kind="Team")


class Project(ndb.Model):
    owner = ndb.KeyProperty(kind="User")
    team = ndb.KeyProperty(kind="Team")
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    date = ndb.StringProperty()
    time_range = ndb.StringProperty()
    location = ndb.StringProperty()
    room_name = ndb.StringProperty()
    status = ndb.IntegerProperty()
    qualifications = ndb.StringProperty()


class ProjectUsers(ndb.Model):
    project = ndb.KeyProperty(kind="Project")
    user = ndb.KeyProperty(kind="User")
    status = ndb.IntegerProperty()


class Team(ndb.Model):
    type = ndb.StringProperty()
