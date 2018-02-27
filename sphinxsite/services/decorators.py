from django.http import HttpResponseForbidden
from sphinxsite import models as sphinx_models

def invite(function):
	'''
	Verify that a given invitation code is valid. To be valid, the first name, 
	last name, email address, and the randomly generated invitation code that 
	was sent to the user before the signup process must match the database
	record.
	'''
	def wrapper(request):
		
		status = 'FAIL'
		params = {
			'code': request.POST.get('invite_code'),
			'first_name': request.POST.get('first_name'),
			'last_name': request.POST.get('last_name'),
			'email': request.POST.get('email'),
			'used': False
		}
		exists = sphinx_models.InviteCode.objects.filter(**params).exists()
		if exists:
			status = 'SUCCESS'
		return function({'status': status})

	return wrapper



def username(function):
	'''
	Check if the selected username during the sign-up process already
	exists in the database. If so, set status to FAIL and SUCCESS otherwise.
	'''

	def wrapper(request):

		status = 'FAIL'
		username = request.POST.get('username')
		params = {'user__username': username}
		exists = sphinx_models.SiteUser.objects.filter(**params).exists()
		if not exists:
			status = 'SUCCESS'
		return function({'status': status})

	return wrapper

def POST_only(function):
	'''
	Verify that an HTTP request is of type POST. Otherwise, return 
	a 403 Forbidden error. View functions with this decorator are usually
	ajax or form submission endpoints. 
	'''

	def wrapper(request):

		if request.method == 'POST':
			return function(request)
		return HttpResponseForbidden()

	return wrapper



