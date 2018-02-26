import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from sphinxsite.services import helper
from sphinxsite import models as sphinx_models

from sphinxsite.services import loggers
logger = loggers.Loggers(__name__).get_logger()




# Workflow:
#     1. User lands on the homepage
#         a. If they're already logged in, they'll be shown the sphinx page
#         b. else if they're not logged in, they'll be shown the login page
#     2. If login succeeds, the sphinx page shown 
#     3. On the login page, option for password reset:
#         -if reset requested, load a new page through ajax to show reset options
#             -reset should redirect to a thankyou page and expire the previous page 
#     4. password reset should take to a password reset page 
#         1. if reset succeeds, redirect to the sphinx page
#     5. On the login page, option for signup:
#         1. redirect to the signup page 
#         2. success or failure should follow signup pages redirection routine
#     6. Logging out
#         -since we can't embed a logout link in a sphinx page, document at the 
#         very beginning of the sphinx page that the only way to logout is to go to 
#         /logout 
#     7. Logout page:
#         -same style as login/signup
#         -say 'you've been logged out, etc. and show a link to go to the login page 

def apidocs(request):
    

    # - make sure the user is logged in first
    # -if user logged in, let them see the apidocs landing page
    #     return a different template and context dict for the sphinx page
    # -else: redirect to the homepage for login
    #     return the login form 
    # return render(request, 'the_sphinx_landing_page.html', {'f': form})
    return render(request, 'login.html', {})


def validate_invite(request):
    '''
    Validate the invite code against what's already in the database. 
    Note: This function is used in an AJAX call before form submission.

    '''
    pass
    # If validation fails, let the client know that it failed possibly because:
    #     1. The invitation code entered is invalid
    #     2. The invitation code may have been redeemed already
    #     3. The invitation code belongs to someone else
    #     4. Solution: Make sure you enter the validation code with first name, last name,
    #         and email address that was indicated in the invitation email
    #     5. The client should be a red x next to the validation code and disable the signup 
    #         button; disply the error message in <li> beneath the input box

    # if validation succeeds:
    #     1. set status to SUCCESS
    #     2. the client should put a green checkmark next to the input box and let the 
    #         signup proceed



def signup(request):
	
    context = helper.process_form_data(request)
    if context.get('status') == 'SUCCESS':
        username = context.get('form_data').get('username')
        raw_password = context.get('form_data').get('password')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('apidocs')
    # elif context['status'] == 'UKNOWN':
        # validation is handled through an ajax call; if it fails, signup is never called,
        # except to populate the initial form
        # pass
        # handle validation failure here

    return render(request, 'signup.html', {'form': context.get('form')})

def username_availability(request):
  
    username = request.POST.get('username')
    exists = sphinx_models.SiteUser.objects.filter(user__username=username).exists()
    response = {'available': exists}
    return JsonResponse(response)

    