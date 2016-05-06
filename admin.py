import logging
import os
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from webapp2_extras import routes

from models import Form

template.register_template_library('templatetags.uri_for')

templates_directory = os.path.join(os.path.dirname(__file__), 'templates')

class FormListHandler(webapp2.RequestHandler):
	def get(self):
		forms = Form.query().fetch(keys_only=True)		
		
		template_values = {
			'form_keys': map(lambda form: form.urlsafe(), forms)
		}
		
		html_template_path = os.path.join(templates_directory, 'admin_forms_list.html')
		html = template.render(html_template_path, template_values)
		
		self.response.write(html)

class BaseFormHandler(webapp2.RequestHandler):
	def _render_form(self, form={}):
		template_values = {
			"form": form
		}
		
		html_template_path = os.path.join(templates_directory, 'admin_form_details.html')
		html = template.render(html_template_path, template_values)
		
		self.response.write(html)
		
	def _update_form_from_request(self, form):
		form.recipient = self.request.POST['recipient']
		form.sender = self.request.POST['sender']
		form.subject = self.request.POST['subject']

class FormDetailsHandler(BaseFormHandler):
	def get(self, key):
		form_key = ndb.Key(urlsafe=key)
		form = form_key.get()
		
		self._render_form(form)
		
	def post(self, key):
		form_key = ndb.Key(urlsafe=key)
		form = form_key.get()
		
		self._update_form_from_request(form)
		
		form.put()
		
		logging.info("Updated form '%s'" % form.key.urlsafe())
		
		self._render_form(form)
		
class FormCreationHandler(BaseFormHandler):
	def get(self):
		self._render_form()
		
	def post(self):
		form = Form()
		self._update_form_from_request(form)
		
		form.put()
		
		logging.info("Created form '%s'" % form.key.urlsafe())
		
		self.redirect(self.uri_for('forms-list'))
		
app = webapp2.WSGIApplication([
	webapp2.Route(r'/admin/forms', handler=FormListHandler),
	webapp2.Route(r'/admin/forms/', handler=FormListHandler, name='forms-list'),
	webapp2.Route(r'/admin/forms/create', handler=FormCreationHandler, name='form-create'),
	webapp2.Route(r'/admin/forms/<:(.+)>', handler=FormDetailsHandler, name='form-details')
])
