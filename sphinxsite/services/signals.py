from django.db.models.signals import post_save, pre_delete, pre_save
import sphinxsite.services.loggers as loggers
from mail.services import mailer
logger = loggers.Loggers(__name__).get_logger()

# TODO: Consolidate InviteSignal, RegistrationSginal

class InviteSignal(object):
	"""
	Signal handler to send an invitation email upon database update. In
	order to send an email, the send_email boolean field needs to be true.
	"""

	def __init__(self, sender, *args, **kwargs):
		self.sender = sender

	def execute(self):
		# We don't need to handle delete since no one else 
		# needs to know about delete

		post_save.connect(self.send_email, sender=self.sender)
		# pre_delete.connect(self.delete, sender=self.sender)

	def send_email(self, instance, **kwargs):

		if instance.send_email:
			mailer.send_invite(instance)

class RegistrationSignal(object):
	"""
	Signal handler to send a signup confirmation email
	"""

	def __init__(self, sender, *args, **kwargs):
		self.sender = sender

	def execute(self):
		# We don't need to handle delete since no one else 
		# needs to know about delete
		
		post_save.connect(self.send_email, sender=self.sender)
		# pre_delete.connect(self.delete, sender=self.sender)

	def send_email(self, instance, **kwargs):

		mailer.signup_confirmation(instance)

