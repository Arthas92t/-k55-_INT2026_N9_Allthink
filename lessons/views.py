# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *

def get_lesson(lessonID = 0, lessonName = ''):
	if cmp(lessonName,'') != 0:
		try:
			return Lesson.objects.get(lessonName=lessonName)
		except Lesson.DoesNotExist:
			return None
	try:
		return Lesson.objects.get(pk=lessonID)
	except Lesson.DoesNotExist:
		return None
	

def createLesson(request):
	message = lessonName =''
	if request.POST:
		lessonName = request.POST.get('lessonName')
		lesson = get_lesson(lessonName = lessonName)
		if lesson is None:
			lesson = Lesson(user = request.user, lessonName=lessonName, numberOfPape=0)
			lesson.save()
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
		else:
			message = 'This lesson has already exist'
	return render_to_response('lessons/new_lesson.html',{'message':message,'lessonName':lessonName})

def deleteLesson(request, lessonID):
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is not None:
		if request.user == lesson.user:
			lesson.delete()
			return HttpResponseRedirect('/index/')
		else:
			message = 'You do not have permission to do that'
	else:
		message = 'This lesson does not exist'
	return render_to_response('lessons/delete_lesson.html',{'message':message})

def editLesson(request, lessonID):
	lesson = get_lesson(lessonID = lessonID)
	lessonName = lessonID
	return render_to_response('lessons/edit_lesson.html',{'lessonName':lessonName})