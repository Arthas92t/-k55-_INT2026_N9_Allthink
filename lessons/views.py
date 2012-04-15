# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *
	
def lessonPermission(request, lesson):
	return request.user == lesson.user
	
def pagePermission(request, page):
	return request.user == page.lesson.user

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
	return render_to_response('lessons/new_lesson.html',{'username': request.user.username,'message':message,'lessonName':lessonName})

def deleteLesson(request, lessonID):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')

	lesson.delete()
	return HttpResponseRedirect('/')

def editLesson(request, lessonID):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	
	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')

	listPage= lesson.getAllPage()
	return render_to_response('lessons/edit_lesson.html',
		{'username': request.user.username, 'lessonID':lessonID,
		'lessonName':lesson.lessonName, 'information':lesson.information,
		'listPage':listPage})

def newPage(request, lessonID, type):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')

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
			lesson.addPage(request, type)
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
	return render_to_response('lessons/new_page.html',{'username': request.user.username,'lessonID':lessonID, 'form':formNewPage, 'type': type})

def editPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')

	if( not pagePermission(request, page)):
		return render_to_response('error/permission_deny.html')

	if page.type == 'video':
		formNewPage = FormVideoPage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'image':
		formNewPage = FormImagePage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'document':
		formNewPage = FormDocumentPage(initial={'title': page.title, 'link': page.link, 'text': page.text})
	if page.type == 'text':
		formNewPage = FormTextPage(initial={'title': page.title, 'text': page.text})
	if page.type == 'step':
		formNewPage = FormStepPage(initial={'title': page.title, 'text': page.text})
	
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
	return render_to_response('lessons/new_page.html',{'username': request.user.username,
		'lessonID':lessonID, 'form':formNewPage,
		'type': type,
		})

def viewPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	
	listPage = lesson.getAllPage()
	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')
	nextPage = 0
	if(int(pageNumber) < len(lesson.getAllPage()) - 1):
		nextPage = int(pageNumber) + 1
	return render_to_response('lessons/view_page.html',{'username': request.user.username,
		'lessonID':lessonID, 'page':page, 'listPage':listPage,
		'type': type, 'nextPage': nextPage,
		})

def deletePage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')

	if( not pagePermission(request, page)):
		return render_to_response('error/permission_deny.html')

	page.delete()
	for i in lesson.getAllPage():
		if (i.pageNumber > int(pageNumber)):
			i.pageNumber = i.pageNumber - 1
			i.save()
	return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')

def upPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')

	if( not pagePermission(request, page)):
		return render_to_response('error/permission_deny.html')

	if (page.pageNumber > 0):
		page1 = lesson.getPage(int(pageNumber) - 1)
		page1.pageNumber = page1.pageNumber + 1
		page.pageNumber = page1.pageNumber - 1
		page.save()
		page1.save()
	return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')

def downPage(request, lessonID, pageNumber):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')
	
	if( not pagePermission(request, page)):
		return render_to_response('error/permission_deny.html')

	if (page.pageNumber < lesson.len() - 1):
		page1 = lesson.getPage(int(pageNumber) + 1)
		page1.pageNumber = page1.pageNumber - 1
		page.pageNumber = page1.pageNumber + 1
		page.save()
		page1.save()
	return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')

def test(request):
	t = '<a href="/lessons/view_page/{{lessonID}}/{{ i.pageNumber + 1 }}/">Next page</a>'
	return render_to_response('lessons/bug.html', {'t': t})