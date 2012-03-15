# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *

def get_lesson(lessonID = 0):
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
		lesson = Lesson(user = request.user, lessonName=lessonName)
		lesson.save()
		return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
	return render_to_response('lessons/new_lesson.html',{'message':message,'lessonName':lessonName})

def deleteLesson(request, lessonID):
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is not None:
		if request.user != lesson.user:
			return render_to_response('error/permission_deny.html')
	else:
		return render_to_response('error/not_found.html')
	lesson.delete()
	return HttpResponseRedirect('/index/')

def editLesson(request, lessonID):
	message =''
	listPage=[]
	listNumber =[]
	lesson = get_lesson(lessonID = lessonID)
	if lesson is not None:
		if request.user != lesson.user:
			return render_to_response('error/permission_deny.html')
	else:
		return render_to_response('error/not_found.html')
	for page in lesson.pageList:
		listPage.append(pape.title)
		listNumber = range(len(lesson.pageList))
	return render_to_response('lessons/edit_lesson.html',
		{'message':message, 'lessonName':lesson.lessonName,
		'listPage':listPage, 'listNumber': listNumber})
