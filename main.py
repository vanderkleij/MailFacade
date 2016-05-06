import logging
import os
import webapp2

from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from models import Form

class MainHandler(webapp2.RequestHandler):
	def get(self, key):
		self.__process_request(key)
		
	def post(self, key):
		self.__process_request(key)
		
	def __process_request(self, key):
		form_key = ndb.Key(urlsafe=key)
		form = form_key.get()

		email_html = self.__render_email_template('html')
		email_text = self.__render_email_template('txt')
		self.__send_email(form, email_html, email_text)
		
		redirect_url = self.request.get('__redirect') or self.request.referer
		
		if redirect_url:
			self.redirect(str(redirect_url))
		else:
			self.response.write(MainHandler.__render_template('thanks.html', {}))
		
	def __send_email(self, form, html, text):		
		message = mail.EmailMessage()
		message.sender = form.sender
		message.subject = form.subject or 'MailFacade: form submitted'
		message.to = form.recipient
		message.body = text
		message.html = html
		
		logging.info("Sending e-mail to '%s'..." % message.to)
		
		message.send()

	def __render_email_template(self, extension):
		valid_pairs = filter(lambda tuple: not tuple[0].startswith('__'), self.request.params.items())
		
		template_values = {
			"pairs": valid_pairs,
		}
		
		return MainHandler.__render_template("email.%s" % extension, template_values)
		
	@staticmethod
	def __render_template(template_file, template_values):
		templates_directory = os.path.join(os.path.dirname(__file__), 'templates')
		template_path = os.path.join(templates_directory, template_file)
		return template.render(template_path, template_values)
	
app = webapp2.WSGIApplication([(r'/([^/]+)', MainHandler)])
