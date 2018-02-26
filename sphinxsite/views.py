from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from sphinxsite.services import helper


def apidocs(request):

    return render(request, 'signup.html', {'f': form})

def signup(request):
	
    context = helper.process_form_data(request)
    if context['success']:
        username = context.get('form_data').get('username')
        raw_password = context.get('form_data').get('password')
        # user = authenticate(username=username, password=raw_password)
        # login(request, user)
        return redirect('apidocs')
    return render(request, 'signup.html', context)


     # if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=raw_password)
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = SignUpForm()