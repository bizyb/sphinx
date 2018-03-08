from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
			'invite_code_input': request.POST.get('invite_code'),
		}
		context['status'] = 'SUCCESS'
		context['form_data'] = record
		msg = "New signup form: {}".format(record)
		logger.info(msg)

	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)
	return context


def create_new_user(user_data, user_model, invite_model):
	'''
	Create a new user with the default privilege level and assign it 
	to a newly created instance of SiteUser, which links invitation code 
	and other attributes to the user. 

	Note: Typically creating a new model object requires using the create() function.
	However, using create() on a User object will result in the password being saved in 
	plain text format. In order for the password to be hashed, we need to use the 
	create_user() method instead.

	Also note that we're passing in the models as function arguments instead of
	inporting the model. This is so that when the helper module is imported by
	models.py, we can avoid circular import issues.
	'''
	user_entry = {

		'first_name': user_data.get('first_name'),
		'last_name': user_data.get('last_name'),
		'email': user_data.get('email'),
		'username': user_data.get('username'),
		'password': user_data.get('password'),
	}
	user_obj = User.objects.create_user(**user_entry)
	invite_obj = None
	try:
		invite_obj = invite_model.objects.filter(code=user_data.get('invite_code_input'))[0]
	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)

	params = {
		'user': user_obj,
		'invite_code_input': user_data.get('invite_code_input'),
		'invite_code': invite_obj,
		'team': user_data.get('team')
	}
	site_user_obj = user_model.objects.create(**params)
	msg = "New user added: {}".format(site_user_obj)
	logger.info(msg)

def user_login(request, username, password):

	success = False
	if username and password:
		credentials = {
			'request': request,
			'username': username,
			'password': password
		}
		user = authenticate(**credentials)
		if user is not None:
			login(request, user)
			success = True
	return success

def get_sphinx_page_type(request):

	return "index.html"

def load_sphinx_page(file_name):

	return "test content"














