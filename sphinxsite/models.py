from __future__ import unicode_literals
# from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

# from django.core.urlresolvers import reverse
# from time import time
# import datetime
# from mptt.models import MPTTModel, TreeForeignKey 
# from django.contrib.postgres.fields import JSONField
# import services.common_helper as common_helper
# import services.signals as signals


class InviteCode(models.Model):
	'''
	Store sign-up invite code. If a new invite code is created, send an email
	to the person the invite code was created for so they can sign up. 

	'''
	code 		= models.CharField(max_length=32)
	first_name 	= models.CharField(max_length=256, blank=False, null=False)
	last_name 	= models.CharField(max_length=256, blank=False, null=False)
	email		= models.EmailField(blank=False, null=False)
	used 		= models.BooleanField(default=False)

	
	def __unicode__(self):

		# Model object name to show in the admin dashboard or in shell queries
		return '%s' % (self.code)

	def save(self, *args, **kwargs):

		if not self.code:
			self.code = helper.get_random_code()

		super(InviteCode, self).save(*args, **kwargs)




class Team(models.Model):

	name = models.CharField(max_length=32, blank=False, null=True)

	def __unicode__(self):

		# Model object name to show in the admin dashboard or in shell queries
		return '%s' % (self.name)



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
	invite_code_input 	= models.CharField(max_length=32, blank=False, null=False)
	invite_code 		= models.ForeignKey(InviteCode, related_name="siteuser_invitecode")
	team 				= models.ForeignKey(Team, related_name="siteuser_team", blank=True, null=True)


	# def validate_code(self):

	# 	code_obj_qset = InviteCode.objects.filter(code=self.invite_code_input)
	# 	if code_obj_qset.exists():

	# 		code_obj = code_obj_set[0] # we expect a single match so it's usually just the first object

	# 		if code_obj.used:
	# 			raise InviteCodeInUse
	# 		valid = code_obj.email == self.user.email && code_obj.first_name == self.user.first_name && 
	# 									code_obj.last_name == self.user.last_name
	# 		if not valid:
	# 			raise ValidationFail
	# 	else:
	# 		raise CodeNotFound

	# 	return True



	def save(self, *args, **kwargs):

		# try:
		# 	self.validate_code()
		# except InviteCodeInUse as e:
		# 	pass
		# except ValidationFail as e:
		# 	pass
		# except CodeNotFound as e:
		# 	pass
		# except Exception as e:
		# 	pass

		self.invite_code = InviteCode.objects.filter(code=invite_code_input)[0]
		self.invite_code.used = True
		self.invite_code.save()

		super(SiteUser, self).save(*args, **kwargs)

