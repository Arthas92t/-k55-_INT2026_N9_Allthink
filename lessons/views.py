# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *

def get_lesson(lessonID = 0, lessonName =''):
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
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	message = lessonName =''
	if request.POST:
		lesson = Lesson(user = request.user, lessonName=request.POST.get('lessonName'), information = request.POST.get('information'))
		lesson.save()
		return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
	return render_to_response('lessons/new_lesson.html',{'request.user.username': request.user.username,'message':message,'lessonName':lessonName})

def deleteLesson(request, lessonID):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is not None:
		if request.user != lesson.user:
			return render_to_response('error/permission_deny.html')
	else:
		return render_to_response('error/not_found.html')
	lesson.delete()
	return HttpResponseRedirect('/')

def editLesson(request, lessonID):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is not None:
		if request.user != lesson.user:
			return render_to_response('error/permission_deny.html')
	else:
		return render_to_response('error/not_found.html')
	
	listPage= lesson.getAllPage()
	return render_to_response('lessons/edit_lesson.html',
		{'request.user.username': request.user.username, 'lessonID':lessonID,
		'lessonName':lesson.lessonName, 'information':lesson.information,
		'listPage':listPage})

def viewLesson(request, lessonID):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	message =''
	listPage=[]
	listNumber =[]
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	return render_to_response('lessons/view_lesson.html',
		{'request.user.username': request.user.username,'lessonID':lessonID, 'message':message, 'lessonName':lesson.lessonName, 'information':lesson.information})

def newPage(request, lessonID, type):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if type == 'video':
		formNewPage = FormVideoPage()
	if type == 'image':
		formNewPage = FormImagePage()
	if type == 'document':
		formNewPage = FormDocumentPage()
	if type == 'text':
		formNewPage = FormTextPage()
	
	if request.POST:
		if type == 'video':
			formNewPage = FormVideoPage(request.POST)
		if type == 'image':
			formNewPage = FormImagePage(request.POST)
		if type == 'document':
			formNewPage = FormDocumentPage(request.POST)
		if type == 'text':
			formNewPage = FormTextPage(request.POST)
		if formNewPage.is_valid():
			lesson.addPage(formNewPage, type)
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
	return render_to_response('lessons/new_page.html',{'request.user.username': request.user.username,'lessonID':lessonID, 'form':formNewPage, 'type': type})

def editPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')
	if page.type == 'video':
		formNewPage = FormVideoPage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'image':
		formNewPage = FormImagePage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'document':
		formNewPage = FormDocumentPage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'text':
		formNewPage = FormTextPage(initial={'title': page.title, 'text': page.text})

	if request.POST:
		if page.type == 'video':
			formPage = FormVideoPage(request.POST)
		if page.type == 'image':
			formPage = FormImagePage(request.POST)
		if page.type == 'document':
			formPage = FormDocumentPage(request.POST)
		if page.type == 'text':
			formPage = FormTextPage(request.POST)
		if formPage.is_valid():
			if not (type == 'text'):
				page.link = formPage.cleaned_data['link']
			page.title = formPage.cleaned_data['title']
			page.text = formPage.cleaned_data['text']
			page.save()
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
	return render_to_response('lessons/new_page.html',{'request.user.username': request.user.username,
		'lessonID':lessonID, 'form':formNewPage,
		'type': type,
		})

def viewPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')
		
	return render_to_response('lessons/view_page.html',{'request.user.username': request.user.username,
		'lessonID':lessonID, 'page':page,
		'type': type,
		})
