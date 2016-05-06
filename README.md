# MailFacade

A simple [Google App Engine](https://cloud.google.com/appengine/) application that sends data posted to it to a preconfigured email address. This is particularly useful for forms on [static sites](https://en.wikipedia.org/wiki/Static_web_page), where there's no database or server-side script to handle the user input. The email address of the recipient of the data is stored within App Engine and not exposed in the HTML, protecting the recipient from spam.

## Getting started

### Deploying to App Engine

Deploying the application to App Engine can be done using the [usual deployment process](https://cloud.google.com/appengine/docs/python/gettingstartedpython27/deploying-the-application) for python App Engine applications. In short, you can use the following steps:

1. Install [Python 2.7](https://www.python.org/).
2. Download the [App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
3. Select or create a new [App Engine project](https://console.cloud.google.com/iam-admin/projects).
4. Clone the MailFacade application repository:

   ```
   git clone https://github.com/vanderkleij/MailFacade.git
   ```

5. From your local repository, run:

   ```
   appcfg.py -A [YOUR_PROJECT_ID] -V v1 update ./
   ```
   
### Using the deployed application

1. Define a new form in the built-in admin interface at `/admin/forms/`. For a typical App Engine project, its full URL is `https://[YOUR_PROJECT_ID].appspot.com/admin/forms`.
   - Specify the recipient of data submitted to the form.
   - Specify the sender address. **Important**: App Engine [imposes restrictions on who can send email](https://cloud.google.com/appengine/docs/python/mail/). Make sure you specify a valid sender.
   - Optionally, specify a subject. If none is provided, a default subject will be used.
2. Note the key (the rather long sequence of alphanumerical characters) of the form that was created.
3. Build an HTML form that submits data to `https://[YOUR_PROJECT_ID].appspot.com/[FORM_KEY]`. Be sure to set the `name` attribute for all inputs. For example:

	```HTML
	<form action="https://yourapp.appspot.com/ag1lfm1haWwtZmFjYWRlchELEgRGb3JtGICAgICAgIAKDA" method="POST">
		<label for="from">Email address:</label>
		<input type="email" name="from" id="from">
	
		<label for="message">Message:</label>
		<textarea name="message" id="message" rows="3"></textarea>
	
		<button type="submit" class="btn btn-default">Submit</button>
	</form>
	```
	
4. Optionally add a hidden input that specifies where the user should be redirected to after submitting the form:

	```HTML
	<input type="hidden" name="__redirect" value="https://www.google.com" />
	```

5. That's it. When you submit the form, you should receive an email message containing the submitted data.