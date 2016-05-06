from google.appengine.ext import ndb

class Form(ndb.Model):
	recipient = ndb.StringProperty(required=True)
	sender = ndb.StringProperty(required=True)
	subject = ndb.StringProperty(required=False)