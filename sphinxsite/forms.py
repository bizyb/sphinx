from sphinxsite import models as sphinx_models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):

	invite_code = forms.CharField(max_length=32, required=True)
	team = forms.CharField(max_length=32)
	# 'invite_code': forms.TextInput(attrs={'placeholder': 'Invite Code', 'name': 'invite_code'}),
	class Meta:
	    model = User
	    widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'name': 'first_name', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'name': 'last_name', 'required': 'True'}),
            'team': forms.TextInput(attrs={'placeholder': 'Team', 'name': 'team', 'required': 'False'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address', 'name': 'email', 'required': 'True'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'name': 'username', 'required': 'True'}),
            
        }
	    fields = [ 'first_name', 'last_name', 'team', 'email', 'username', 'password1', 'password2']
