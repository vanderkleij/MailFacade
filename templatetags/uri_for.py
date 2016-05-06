import logging
import webapp2

from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.simple_tag
def uri_for(route, param1=None, param2=None, param3=None):
	args = filter(lambda param: param != None, [param1, param2, param3])
	return webapp2.uri_for(route, None, *args)