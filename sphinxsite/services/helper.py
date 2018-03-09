from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.contrib.auth import authenticate, login
from sphinxsite.services import loggers
from sphinxsite.models import SphinxConfig
from bs4 import BeautifulSoup
import os

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

def _get_sphinx_file_path(request):

	'''
	Parse the url of a request to build an absolute path for a sphinx 
	file stored locally.

	E.g.
		requested url = http://api.perfit.info/apidocs/_sources/genindex.html 
		landing_url = apidocs
		current_url = _sources/genindex.html
		file_path = sphinx_root_dir/current_url

	'''
	
	landing_url = resolve(request.path_info).url_name
	current_url = request.build_absolute_uri()
	current_url = current_url.split(landing_url + "/")[-1]

	filename, file_extension = os.path.splitext(current_url)	
	root_dir = SphinxConfig.objects.all()[0].root_dir

	if not filename:
		# filename should be empty if we're on the landing page

		current_url = "index.html"

	file_path = root_dir + "/" + current_url

	if "search.html" in file_path:
		# if search page is requested, the request could contain a GET 
		# querystring in its path, which needs to be truncated
		file_path = file_path.split("search.html")[0] + "search.html"

	if "highlight=" in file_path:
		# If highlight is enabled (usually happens when the user clicks on 
		# a search result, highlight=search_term querystring is added to the 
		# url. We need to remove them. It doesn't effect the behavior of
		# the page generated because the querystring is only used by the 
		# client js to do its job.  
		file_path = file_path.split("?")[0]

	return file_path

	
def _sphinx_load_error():
	'''
	Generate an html error message if Django has failed to load a 
	sphinx page.
	'''
	msg = "Failed to load page. Please contact the Backend Team if the problem continues "
	msg += "with the url of this page. ERROR 499"
	style = """
			width: 600px;
			text-align: center;
			margin: 0 auto;
			padding-top: 50px;
			color: #fff;
			"""
	html = """
			<div class="sphinx-page-load-error"><p style="{}">{}</p></div> 
		"""
	html = html.format(style, msg)

	return html

def _parse_html(raw, file_path):
	'''
	Parse raw html file and return all the content contained within
	the body tag. If the raw file is not an HTML file, return it as is. 
	'''
	filename, file_extension = os.path.splitext(file_path)

	body = raw
	if file_extension == ".html":
		soup = BeautifulSoup(raw, 'lxml')
		body = soup.find("body")
		body = str(body).replace("<body>", "").replace("</body>", "")

	return body

def load_sphinx_page(request):

	file_path = _get_sphinx_file_path(request)	
	html = _sphinx_load_error()

	try:
		with open(file_path, "r") as f:
			html_raw = f.read()
			html = _parse_html(html_raw, file_path)
			
	except Exception as e:
		msg = '{}: {}'.format(type(e).__name__, e.args[0])
		logger.exception(msg)
		
	return html

def sphinx_search_index(request):
	return True

	














