from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login
from lessons.models import *
from account.models import *
from django import forms


from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
	loginMessage = "Please login below..."
	username = password = ''
	regMessage = "fill all field below"
	formReg = FormRegister()
	
	return render_to_response('account/login.html',{'loginMessage':loginMessage, 'regMessage':regMessage, 'formReg': formReg})

@login_required
def homePage(request):
	yourLessons = []
	otherLessons = []
	username = request.user.username
	for obj in Lesson.objects.all():
		if cmp(obj.user.username,username):
			otherLessons.append(obj)
		else:
			yourLessons.append(obj)
	return render_to_response('index.html',{'username': username,'yourLessons': yourLessons,'otherLessons': otherLessons})

def index(request):
	if request.user.is_authenticated():
		return homePage(request)
	return loginPage(request)