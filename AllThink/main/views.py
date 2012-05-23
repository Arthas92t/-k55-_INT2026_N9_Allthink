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
	formReg = FormRegister()
	
	return render_to_response('account/login.html',{'loginMessage':loginMessage, 'formReg': formReg})

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
	return render_to_response('index.html',{'username': request.user, 'profile':getProfile(request.user),'yourLessons': yourLessons,'otherLessons': otherLessons})

def index(request):
	if request.user.is_authenticated():
		return homePage(request)
	return loginPage(request)

@login_required
def searchLessons(request, keyWord = '', subject='', level = ''):
	otherLessons = []
	if request.POST:
		keyWord = request.POST['keyWord']
		subject = request.POST['subject']
		level = request.POST['level']
		for i in Lesson.objects.all():
			if(((keyWord in i.name)or(keyWord in i.user.username))
				and((subject == i.subject)or(subject ==''))
				and((level == i.level)or(level ==''))
				and(not request.user in i.userJoined.all())
				and(request.user != i.user)):
				otherLessons.append(i)
	return render_to_response('account/search_lessons.html',{
		'username': request.user, 'profile':getProfile(request.user), 'otherLessons': otherLessons,
		'keyWord':keyWord, 'subject': subject,
		'level':level,
		})

@login_required
def help(request):
	return render_to_response('help.html',{"username": request.user})
	
def aboutUs(request):
	return render_to_response('about_us.html',{"username": request.user})
	
