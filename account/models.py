from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core import validators

def get_user(username):
	try:
		return User.objects.get(username=username)
	except User.DoesNotExist:
		return None

def get_email(email):
	try:
		return User.objects.get(email=email)
	except User.DoesNotExist:
		return None

def checkUsername(value):
	user = get_user(value)
	if user is not None:
		raise ValidationError(u'username has already existed')

def checkEmail(value):
	user = get_email(value)
	if user is not None:
		raise ValidationError(u'email has already used')

class FormRegister(forms.Form):
	username = forms.CharField(max_length = 30, label='Username: ', validators = [checkUsername])
	password = forms.CharField(widget=forms.PasswordInput, max_length = 30, label='Password')
	confirmPassword = forms.CharField(widget=forms.PasswordInput, max_length = 30, label='Confirm password: ')
	email = forms.EmailField(label = 'your email: ', validators = [checkEmail])