# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from lessons.models import *
from account.models import *
from django.contrib.auth.decorators import login_required

@login_required
def createLesson(request):
	lessonForm = LessonForm()
	lessonForm.fields['subject'].initial = ''
	lessonForm.fields['level'].initial = ''
	if request.POST:
		lessonForm = LessonForm(request.POST)
		if lessonForm.is_valid():
			lesson = Lesson(
				user = request.user,
				name= lessonForm.cleaned_data['name'],
				subject = lessonForm.cleaned_data['subject'],
				level = lessonForm.cleaned_data['level'],
				information = lessonForm.cleaned_data['information'],
				)
			lesson.save()
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
	return render_to_response('lessons/new_lesson.html',{'username': request.user, 'profile':getProfile(request.user),'lessonForm':lessonForm})

@login_required
def editLessonInfo(request, lessonID):
	message =''
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')

	if( not lessonPermission(request, lesson)):
		return render_to_response('error/permission_deny.html')
	lessonForm = LessonForm(initial={
		'name':lesson.name, 'subject':lesson.subject,
		'level':lesson.level, 'information':lesson.information,
		})
	lessonForm.fields['subject'].initial = lesson.subject
	lessonForm.fields['level'].initial = ''
	if request.POST:
		lessonForm = LessonForm(request.POST)
		if lessonForm.is_valid():
			lesson.name= lessonForm.cleaned_data['name']
			lesson.subject = lessonForm.cleaned_data['subject']
			lesson.level = lessonForm.cleaned_data['level']
			lesson.information = lessonForm.cleaned_data['information']
			lesson.save()
			return HttpResponseRedirect('/lessons/edit_lesson/'+str(lesson.id)+'/')
	return render_to_response('lessons/edit_info.html',{'username': request.user, 'profile':getProfile(request.user),'lessonForm':lessonForm,'lesson':lesson})

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
		{'username': request.user, 'profile':getProfile(request.user), 'lesson':lesson,
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
	return render_to_response('lessons/new_page.html',{'username': request.user, 'profile':getProfile(request.user),
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
	return render_to_response('lessons/new_page.html',{'username': request.user, 'profile':getProfile(request.user),
		'lessonID':lessonID, 'form':result['form'],
		})

@login_required
def viewPage(request, lessonID, pageNumber):
	lesson = get_lesson(lessonID = lessonID)
	if lesson is None:
		return render_to_response('error/not_found.html')
	
	listPage = lesson.getAllPage()
	page = lesson.getPage(pageNumber)
	bonus = []
	if page is not None:
		if page.type == "step":
			bonus = page.getAllStep()
	
	previousPage = int(pageNumber) - 1
	nextPage = 0
	if(int(pageNumber) < len(lesson.getAllPage()) - 1):
		nextPage = int(pageNumber) + 1
	return render_to_response('lessons/view_page.html',{'username': request.user, 'profile':getProfile(lesson.user), 'lesson':lesson,
		'page':page, 'listPage':listPage,
		'previousPage': previousPage, 'nextPage': nextPage,
		'bonus':bonus
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