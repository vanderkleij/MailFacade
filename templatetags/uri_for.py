import webapp2

from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.simple_tag
def uri_for(route, param1=None, param2=None, param3=None):
	# The Django version used by App Engine does not support *args or **kwargs
	# in its template engine. Hence the poor man's *args solution with 
	# a maximum of 3 arguments.
	return webapp2.uri_for(route, None, *[param1, param2, param3])