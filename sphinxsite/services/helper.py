from sphinxsite import models as sphinx_models
from sphinxsite.forms import SignUpForm
from sphinxsite.services import loggers
logger = loggers.Loggers(__name__).get_logger()


def process_form_data(request):
	'''
	If no form submission, return form fields. Otherwise, clean the form data 
	and save it to the database. Return a context dictionary to populate 
	post-submission messages or perform redirects.
	'''
	context = {'status': 'UKNOWN'}
	try:
		if request.method == 'GET':
			f = SignUpForm() 
		else:
			f = SignUpForm(request.POST or None) 
			if f.is_valid():
				record = {
					'first_name': f.cleaned_data.get('first_name'),
					'last_name': f.cleaned_data.get('last_name'),
					'email': f.cleaned_data.get('email'),
					'username': f.cleaned_data.get('username'),
					'password': f.cleaned_data.get('password1'),
					'team': f.cleaned_data.get('team'),
					'invite_code': f.cleaned_data.get('invite_code'),
				}
				# save the form to the db
				sphinx_models.SiteUser.objects.create(**record)
				context['status'] = 'SUCCESS'
				context['form_data'] = entry
				msg = "New signup form: {}".format(record)
				logger.info(msg)
		context['form'] = f
	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)
	return context