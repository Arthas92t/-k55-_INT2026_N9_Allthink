from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core import validators
from django.forms.widgets import *

def getProfile(user):
	profile = None
	for i in user.profile_set.all():
		profile = i
	if profile is None:
		profile = Profile()
		profile.user = user
		profile.save()
	return profile

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

def checkImage(value):
	if value=="":
		return
	a = value.name.split(".")
	a = a[len(a)-1]
	if not((a == "jpg")or(a == "png")or(a == "ico")or(a == "JPG")or(a == "PNG")or(a == "ICO")):
		raise ValidationError(u'allow only jpg, png, ico file')

class FormProfile(forms.Form):
	information = forms.CharField(max_length = 200, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Information', required=False)
	file = forms.FileField(label = 'Avatar', required=False, validators = [checkImage])

def content_file_name(instance, filename):
    return '/'.join(['content', instance.user.username, filename])
	
class Profile(models.Model):
	user = models.ForeignKey(User)
	information = models.CharField(max_length=200)
	file = models.FileField(upload_to = content_file_name)
	def uploadFile(self, request):
		self.file = request.FILES['file']
		self.save()
	
class FormRegister(forms.Form):
	username = forms.CharField(max_length = 30, label='Username: ', validators = [checkUsername])
	password = forms.CharField(widget=forms.PasswordInput, max_length = 30, label='Password')
	confirmPassword = forms.CharField(widget=forms.PasswordInput, max_length = 30, label='Confirm password: ')
	email = forms.EmailField(label = 'your email: ', validators = [checkEmail])