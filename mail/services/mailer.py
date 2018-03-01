from mail.templates import invitation, registration
from django.core.mail import EmailMultiAlternatives
from documentation import settings

import sphinxsite.services.loggers as loggers
logger = loggers.Loggers(__name__).get_logger()

def send_invite(model_obj):
	'''
	Compose an invitation email for account creation. 
	'''
	html_template = invitation.get_template("html")
	txt_template = invitation.get_template("txt")

	sender = settings.EMAIL_SENDER
	subject = "Invitation to Access Perfit API Documentation"

	first_name = model_obj.first_name
	last_name = model_obj.last_name
	recipient = model_obj.email
	invite = model_obj.code

	html_content = html_template.format(first_name, first_name, last_name, recipient, invite)
	txt_content = txt_template.format(first_name, first_name, last_name, recipient, invite)

	try:
		email = EmailMultiAlternatives(subject, txt_content, sender, [recipient])
		email.attach_alternative(html_content, "text/html")
		email.send()

		msg = "Sent a new invitation email to {} {} at {}"
		msg = msg.format(first_name, last_name, recipient)
		logger.info(msg)

	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)

def signup_confirmation(model_obj):

	txt_template = registration.get_template()

	sender = settings.EMAIL_SENDER
	subject = "Welcome to Perfit API Documentation"

	first_name = model_obj.first_name()
	last_name = model_obj.last_name()
	username = model_obj.username()
	recipient = model_obj.email()

	txt_content = txt_template.format(first_name, username)

	try:
		email = EmailMultiAlternatives(subject, txt_content, sender, [recipient])
		email.send()

		msg = "Sent a registration confirmation to {} {} at {}"
		msg = msg.format(first_name, last_name, recipient)
		logger.info(msg)

	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)

def password_reset(request):
	
	email = request.POST.get("email")






	




