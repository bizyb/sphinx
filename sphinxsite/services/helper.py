from sphinxsite import models as sphinx_models
from sphinxsite.services import loggers
logger = loggers.Loggers(__name__).get_logger()


def process_form_data(request):
	'''
	If no form submission, return form fields. Otherwise, clean the form data 
	and save it to the database. Return a context dictionary to populate 
	post-submission messages or perform redirects.
	'''
	context = {'status': 'FAIL'}
	try:
		record = {
			'first_name': request.POST.get('first_name'),
			'last_name': request.POST.get('last_name'),
			'email': request.POST.get('email'),
			'username': request.POST.get('username'),
			'password': request.POST.get('password1'),
			'team': request.POST.get('team'),
			'invite_code': request.POST.get('invite_code'),
		}
		# save the form to the db
		# sphinx_models.SiteUser.objects.create(**record)
		context['status'] = 'SUCCESS'
		context['password'] = record.get('password')
		context['username'] = record.get('username')

		msg = "New signup form: {}".format(record)
		logger.info(msg)

	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)
	return context

