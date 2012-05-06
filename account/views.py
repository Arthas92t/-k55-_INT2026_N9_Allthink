# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from account.models import *
from django import forms
from lessons.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
		
def filePermission(request, file):
	return request.user == file.user

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
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
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
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

@login_required
def fileManager(request):
	formFile = FormFile()
	if request.FILES:
		file = UserFile()
		file.uploadFile(request)
		file.save()
		return HttpResponseRedirect('/file_manager/')
	allFiles = request.user.userfile_set.all()
	return render_to_response('account/file_manager.html',{'user':request.user, 'files':allFiles, 'upload':formFile})

@login_required
def deleteFile(request, fileID):
	file = get_file(fileID)
	if not filePermission(request, file):
		return render_to_response('error/permission_deny.html')
	file.file.delete();
	file.delete()
	return HttpResponseRedirect('/file_manager/')
	
@login_required
def yourLessons(request):
	yourLessons = []
	user = request.user
	return render_to_response('account/your_lessons.html',{'username': request.user, 'yourLessons': user.lesson_set.all()})

@login_required
def searchLessons(request, keyWord = ''):
	otherLessons = []
	if request.POST:
		keyWord = request.POST['keyWord']
	if keyWord:
		for i in Lesson.objects.all():
			if((keyWord in i.name)or(keyWord in i.user.username))and(not request.user in i.userJoined.all()):
				otherLessons.append(i)
	return render_to_response('account/search_lessons.html',{'username': request.user, 'otherLessons': otherLessons, 'keyWord':keyWord})

@login_required
def joinLesson(request, lessonID, keyWord):
	lesson = get_lesson(lessonID = lessonID)
	lesson.userJoined.add(request.user)
	lesson.save()
	return searchLessons(request, keyWord)

@login_required
def unjoinLesson(request, lessonID):
	lesson = get_lesson(lessonID = lessonID)
	lesson.userJoined.remove(request.user)
	lesson.save()
	return lessonsJoined(request)

@login_required
def lessonsJoined(request):
	lessons = []
	user = request.user
	for i in user.lessonsjoined.all():
		if i.user != request.user:
			lessons.append(i)
	return render_to_response('account/lessons_joined.html',{'username': request.user, 'lessons':lessons})
