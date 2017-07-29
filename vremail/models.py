from google.appengine.ext import ndb

class Mail(ndb.Model):
    user_ID = ndb.StringProperty(required=True)
    od = ndb.StringProperty(required=True)
    do = ndb.StringProperty(required=True)
    sporocilo = ndb.TextProperty(required=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    izbrisani_id = ndb.StringProperty(required=True)
    izbrisan = ndb.BooleanProperty(default=False)
