from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from services import signals


class SphinxConfig(models.Model):
	'''
	Stores the current configuration settings for the sphinx pages. 

	Because Sphinx is its own engine that generates html files that can be served
	separately on an external website, serving those html pages through Django 
	is tricky. The trickiness comes from the fact that Sphinx has its own static
	file references for css and javascript. In addition, it has a bunch of embedded 
	URLS that lead to more documentation and source code. Thankfully, all the URLs
	are self-contained, meaning that they point to files somewhere in the sphinx 
	directory. In order to serve them natively through Django, we need to be 
	able to figure out where the sphinx root directory is for all sphinx-related
	files. We can hardcode the root directory into the helper module that loads
	the pages but that's not very user friendly. Instead, we want to make it 
	possible for anyone to update the directory path. In addition, from a design
	point of view, this would keep sphinx strictly independent of Django. That 
	means wherever the sphinx engine is located, we can got there and issue 
	'make html', which would generate the most up-to-date documentation. This may 
	generate brand new html pages or add .rst or .txt files. As far as Django is 
	concerned, they are just local files that need to be imported. 

	This approach solves the problem of embedding an externally hosted documentation
	site in an iframe. Embedding it defeats the purpose of having a Django site 
	with registration and login requirements because anyone can just follow the iframe
	source url and load the page without having to login or register. This approach 
	ensures that the only way to access the documentation site is through the portal.
	
	If the root directory is not set properly, Django will fail to load the documentation
	site.

	TODO: Add more config fields as needed and update admin.py.
	'''

	help_text = "Root directory of sphinx-generated files. Eg. ../_build_html/html"
	help_text += " where .. is the path to the parent directory"
	root_dir = models.CharField(max_length=256)

	def __unicode__(self):
		return '%s' % (self.root_dir)



class InviteCode(models.Model):
	'''
	Store sign-up invite code. If a new invite code is created, send an email
	to the person the invite code was created for so they can sign up. 

	'''
	code 		= models.CharField(max_length=64)
	first_name 	= models.CharField(max_length=256, blank=False, null=False)
	last_name 	= models.CharField(max_length=256, blank=False, null=False)
	email		= models.EmailField(blank=False, null=False)
	in_use 		= models.BooleanField(default=False)
	send_email	= models.BooleanField(default=False)

	
	def __unicode__(self):

		# the toString() equivalent
		label = "{} {} {}".format(self.first_name, self.last_name, self.email)
		return '%s' % (label)

	def save(self, *args, **kwargs):

		if not self.code:
			self.code = str(uuid4())

		super(InviteCode, self).save(*args, **kwargs)




class SiteUser(models.Model):
	'''
	Store user profile. Extend Django's default fields such as username, password, email,
	and etc. and add additional fields to validate invite code. Verify that user info, 
	such as first name, last name, and email, provided by the user during the sign-up 
	process match the information that was provided to generate the invite code. If 
	invite code cannot be validated, do not create a new user profile. Instead, raise 
	invalid invitation code error (invalid either because the code has already been 
	used or because user-provided information could not be validated).
	'''

	user 				= models.OneToOneField(User, on_delete=models.CASCADE)
	invite_code_input 	= models.CharField(max_length=64, blank=False, null=False)
	invite_code 		= models.ForeignKey(InviteCode, related_name="siteuser_invitecode", null=True)
	team 				= models.CharField(max_length=64, blank=True, null=False)


	def first_name(self):
		return self.user.first_name

	def last_name(self):
		return self.user.last_name

	def email(self):
		return self.user.email

	def invite(self):
		return self.invite_code_input

	def username(self):
		return self.user.username


# handle updates to the db
invite_signal_obj = signals.InviteSignal(InviteCode)
signup_signal_obj = signals.RegistrationSignal(SiteUser)
invite_signal_obj.execute()
signup_signal_obj.execute()

