from mail.templates import invitation
from django.core.mail import EmailMultiAlternatives
from documentation import settings

def send_invite(model_obj=None):
	'''
	Compose an invitation email for account creation. 
	'''
	html_template = invitation.get_template("html")
	txt_template = invitation.get_template("txt")

	sender = settings.EMAIL_SENDER
	subject = "Invitation to Access Perfit API Documentation"

	first_name = model_obj.first_name()
	last_name = model_obj.last_name()
	recipient = model_obj.email()
	invite = model_obj.invite()

	# first_name = "Sideshow"
	# last_name = "Bob"
	# recipient = "melesse@usc.edu"
	# invite = "e8b46ad5-45f4-4bda-990b-29206351a6ab"

	html_content = html_template.format(first_name, first_name, last_name, recipient, invite)
	txt_content = txt_template.format(first_name, first_name, last_name, recipient, invite)

	email = EmailMultiAlternatives(subject, txt_content, sender, [recipient])
	email.attach_alternative(html_content, "text/html")
	email.send()





# 	subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()


# 	msg = EmailMessage('Perfit Email Test', 'It Works!', , ['melesse@usc.edu'])





