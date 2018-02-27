from __future__ import unicode_literals
# from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# from django.core.urlresolvers import reverse

# import services.signals as signals


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

		# Model object name to show in the admin dashboard or in shell queries
		return '%s' % (self.code)

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
	invite_code 		= models.ForeignKey(InviteCode, related_name="siteuser_invitecode")
	team 				= models.CharField(max_length=64, blank=True, null=False)


	def first_name(self):
		return self.user.first_name

	def last_name(self):
		return self.user.last_name

	def email(self):
		return self.user.email

	def invite(self):
		return self.invite_code_input
