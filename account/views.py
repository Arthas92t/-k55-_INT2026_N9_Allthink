# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from account.models import *
from django import forms

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
		
def register(request):
	loginMessage = "Please login below..."
	regMessage = "fill all field below"
	formReg = FormRegister()
	if request.POST:
		formReg = FormRegister(request.POST)
		if formReg.is_valid():
			username = formReg.cleaned_data['username']
			password = formReg.cleaned_data['password']
			confirmPassword = formReg.cleaned_data['confirmPassword']
			email = formReg.cleaned_data['email']
			if cmp(password, confirmPassword) ==0:
				user = User.objects.create_user(username,email,password)
				permission = Permission.objects.get(codename="add_lesson")
				user.user_permissions.add(permission)
				user.is_staff = True
				user.save()

				user = authenticate(username=username, password=password)
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				regMessage = 'password and confirm password are not the same'
	return render_to_response('account/login.html',{'loginMessage':loginMessage, 'regMessage':regMessage, 'formReg': formReg})
	
def logout_user(request):
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect('/')

def login_user(request):
	loginMessage = "Please login below..."
	regMessage = "fill all field below"
	username = password = ''
	formReg = FormRegister()
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		if user is not None:
				login(request, user)
				return HttpResponseRedirect('/')
		else:
			loginMessage = "Your username and/or password were incorrect."
			
	return render_to_response('account/login.html',{'loginMessage':loginMessage, 'regMessage':regMessage, 'formReg': formReg})
