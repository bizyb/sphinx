from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from sphinxsite.services import helper, decorators
from sphinxsite import models as sphinx_models
from sphinxsite.services import loggers
logger = loggers.Loggers(__name__).get_logger()

# @login_required
def apidocs(request):
   
    page_type = helper.get_sphinx_page_type(request)
    html = helper.load_sphinx_page(page_type)
    context = {"html_content": html}
    return render(request, "sphinx.html", context)


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
        username = context.get('form_data').get('username')
        password = context.get('form_data').get('password')
        helper.user_login(request, username, password)

    return JsonResponse({'status': context.get('status')})



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        success = helper.user_login(request, username, password)

        if success:
            return HttpResponseRedirect("apidocs")
        else:
            # return value not used by the client
            return JsonResponse({'status': 'FAIL'})                

    if request.user.is_authenticated:
        return redirect('apidocs')
    else:
        return render(request, 'login.html', {})

def logout_view(request):

    logout(request)
    return HttpResponseRedirect("/")

@decorators.POST_only
def password_reset_view(request):
    return JsonResponse({'status': 'SUCCESS'})




@decorators.POST_only
@decorators.username
def username_availability(request):
    '''
    Note: The original request object is a data structure with all the HTTP 
    attributes. However, the request returned by the decorator is a dictionary.
    '''
    return JsonResponse(request)

    
