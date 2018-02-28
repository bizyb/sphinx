from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from sphinxsite.services import helper, decorators
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



@login_required
def apidocs(request):
   
    return render(request, 'sphinx.html', {})


@decorators.POST_only
@decorators.invite
def validate_invite(request):
    '''
    Validate the invite code against what's already in the database. 
    Note: This function is used in an AJAX call before form submission.
    
    The original request object is a data structure with all the HTTP 
    attributes. However, the request returned by the decorator is a dictionary.
    '''
    return JsonResponse(request)


@decorators.POST_only
def registration(request):

    context = helper.process_form_data(request)
    if context.get('status') == 'SUCCESS':
        # create a new user
        su = sphinx_models.SiteUser
        ic = sphinx_models.InviteCode
        helper.create_new_user(context.get('form_data'), su, ic)

        
    return JsonResponse({'status': context.get('status')})


def login(request):

    # re-direct if user already logged in 
    if request.method == "POST":
        print request.POST
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request=request, username=username, password=password)
            print "user-------------: ", user
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect("apidocs") 
                # return redirect('apidocs')
                # return JsonResponse({'status': 'SUCCESS'})
            else:

                return JsonResponse({'status': 'FAIL'})

    if request.user.is_authenticated:
        return redirect('apidocs')
    else:
        return render(request, 'login.html', {})



@decorators.POST_only
@decorators.username
def username_availability(request):
    '''
    Note: The original request object is a data structure with all the HTTP 
    attributes. However, the request returned by the decorator is a dictionary.
    '''
    print '-----------------request: ', request
    return JsonResponse(request)

    