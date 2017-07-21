from google.appengine.ext import ndb

class Mail(ndb.Model):
    od = ndb.StringProperty(required = True)
    do = ndb.StringProperty(required = True)
    sporocilo = ndb.TextProperty(required = True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)
    prejeto = ndb.BooleanProperty()
    izbrisan = ndb.BooleanProperty(default=False)


class Vreme(ndb.Model):
    naslov_filma = ndb.StringProperty(required = True)
    IMDB_link = ndb.TextProperty()
    edited_by = ndb.StringProperty(required = True)
    ocena = ndb.IntegerProperty(required = True)
    updated_on = ndb.DateTimeProperty(auto_now_add=True)