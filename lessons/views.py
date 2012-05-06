# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *
from django.contrib.auth.decorators import login_required

@login_required
def createLesson(request):
	message = name =''
	if request.POST:
		lesson = Lesson(user = request.user, name=request.POST.get('name'), information = request.POST.get('information'))
		lesson.save()
		return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
	return render_to_response('lessons/new_lesson.html',{'username': request.user,'message':message})

@login_required
def deleteLesson(request, lessonID):
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')

	lesson.delete()
	return HttpResponseRedirect('/your_lessons/')

@login_required
def editLesson(request, lessonID):
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	
	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')

	listPage= lesson.getAllPage()
	return render_to_response('lessons/edit_lesson.html',
		{'username': request.user, 'lesson':lesson,
		'information':lesson.information,'listPage':listPage})

@login_required
def newPage(request, lessonID, type):
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')
	
	result = lesson.addPage(request, type)
	if result['accept']:
		return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
	return render_to_response('lessons/new_page.html',{'username': request.user.username,
		'lessonID':lessonID, 'form':result['form'],
		})

@login_required
def editPage(request, lessonID, pageNumber):
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	page = lesson.getPage(pageNumber)
	if page is None:
		return render_to_response('error/not_found.html')

	if( not pagePermission(request, page)):
		return render_to_response('error/permission_deny.html')

	result = page.editPage(request)
	if result['accept']:
		return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
	return render_to_response('lessons/new_page.html',{'username': request.user.username,
		'lessonID':lessonID, 'form':result['form'],
		})

@login_required
def viewPage(request, lessonID, pageNumber):
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	
	listPage = lesson.getAllPage()
	page = lesson.getPage(pageNumber)
	previousPage = int(pageNumber) - 1
	nextPage = 0
	if(int(pageNumber) < len(lesson.getAllPage()) - 1):
		nextPage = int(pageNumber) + 1
	return render_to_response('lessons/view_page.html',{'username': request.user, 'lesson':lesson,
		'page':page, 'listPage':listPage,
		'previousPage': previousPage, 'nextPage': nextPage,
		})

@login_required
def deletePage(request, lessonID, pageNumber):
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

@login_required
def upPage(request, lessonID, pageNumber):
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

@login_required
def downPage(request, lessonID, pageNumber):
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
	t = isinstance(HttpResponseRedirect('/'),HttpResponseRedirect)
	return render_to_response('lessons/bug.html', {'t': t})