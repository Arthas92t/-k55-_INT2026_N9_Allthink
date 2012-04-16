from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
# Create your models here.

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

class Lesson(models.Model):
	user = models.ForeignKey(User)
	lessonName = models.CharField(max_length=200)
	information = models.CharField(max_length=1000)
	
	def __unicode__(self):
		return self.lessonName
	
	def addPage(self, request, type):
		if type == 'video':
			newPage = VideoPage()
		if type == 'image':
			newPage = ImagePage()
		if type == 'document':
			newPage = DocumentPage()
		if type == 'text':
			newPage = TextPage()
		if type == 'step':
			newPage = StepPage()

		newPage.lesson = self
		newPage.type = type
		newPage.pageNumber = self.len()
		
		return newPage.editPage(request, self.id)
		
	def getAllPage(self):
		listPage = []
		for i in self.videopage_set.all():
			listPage.append(i)
		for i in self.imagepage_set.all():
			listPage.append(i)
		for i in self.documentpage_set.all():
			listPage.append(i)
		for i in self.textpage_set.all():
			listPage.append(i)
		for i in self.steppage_set.all():
			listPage.append(i)
		for i in range(len(listPage)):
			for j in range(i, len(listPage)):
				if(listPage[i].pageNumber > listPage[j]. pageNumber):
					temp = listPage[i]
					listPage[i] = listPage[j]
					listPage[j] = temp
		return listPage
	
	def len(self):
		return len(self.getAllPage())
		
	def getPage(self, number):
		return self.getAllPage()[int(number)]
	
class FormVideoPage(forms.Form):
	title = forms.CharField(max_length=200)
	link = forms.CharField(max_length = 1000, label = 'Video URL')
	text = forms.CharField(max_length = 1000, label = 'Text (Optional)', required=False)

class VideoPage(models.Model):
	lesson = models.ForeignKey(Lesson)

	title = models.CharField(max_length=200)
	link = models.CharField(max_length=1000)
	text = models.CharField(max_length=1000, blank = True)

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title
	
	def linkID(self):
		return self.link[(len(self.link) - 11):]

	def editPage(self, request, lessonID):
		formNewPage = FormVideoPage(initial={'title': self.title, 'link': self.link, 'text': self.text})
		
		if request.POST:
			formPage = FormVideoPage(request.POST)
			if formPage.is_valid():
				self.link = formPage.cleaned_data['link']
				self.title = formPage.cleaned_data['title']
				self.text = formPage.cleaned_data['text']
				self.save()
				return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
		return render_to_response('lessons/new_page.html',{'username': request.user.username,
			'lessonID':lessonID, 'form':formNewPage,
			'type': type,
			})

class FormImagePage(forms.Form):
	title = forms.CharField(max_length=200)
	link = forms.CharField(max_length = 1000, label = 'Image URL')
	text = forms.CharField(max_length = 1000, label = 'Text (Optional)', required=False)

class ImagePage(models.Model):
	lesson = models.ForeignKey(Lesson)

	title = models.CharField(max_length=200)
	link = models.CharField(max_length=1000)
	text = models.CharField(max_length=1000, blank = True)

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title

	def editPage(self, request, lessonID):
		formNewPage = FormImagePage(initial={'title': self.title, 'link': self.link, 'text': self.text})
		
		if request.POST:
			formPage = FormImagePage(request.POST)
			if formPage.is_valid():
				if not (type == 'text'):
					self.link = formPage.cleaned_data['link']
				self.title = formPage.cleaned_data['title']
				self.text = formPage.cleaned_data['text']
				self.save()
				return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
		return render_to_response('lessons/new_page.html',{'username': request.user.username,
			'lessonID':lessonID, 'form':formNewPage,
			'type': type,
			})

class FormDocumentPage(forms.Form):
	title = forms.CharField(max_length=200)
	link = forms.CharField(max_length = 1000, label = 'Document URL')
	text = forms.CharField(max_length = 1000, label = 'Text (Optional)', required=False)

class DocumentPage(models.Model):
	lesson = models.ForeignKey(Lesson)

	type = models.CharField(max_length=200)
	link = models.CharField(max_length=1000)
	text = models.CharField(max_length=1000, blank = True)

	title = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title

	def editPage(self, request, lessonID):
		formNewPage = FormDocumentPage(initial={'title': self.title, 'link': self.link, 'text': self.text})
		
		if request.POST:
			formPage = FormDocumentPage(request.POST)
			if formPage.is_valid():
				self.link = formPage.cleaned_data['link']
				self.title = formPage.cleaned_data['title']
				self.text = formPage.cleaned_data['text']
				self.save()
				return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
		return render_to_response('lessons/new_page.html',{'username': request.user.username,
			'lessonID':lessonID, 'form':formNewPage,
			'type': type,
			})

class FormTextPage(forms.Form):
	title = forms.CharField(max_length=200)
	text = forms.CharField(max_length = 1000, label = 'Text')

class TextPage(models.Model):
	lesson = models.ForeignKey(Lesson)

	title = models.CharField(max_length=200)
	text = models.CharField(max_length=1000, blank = True)

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title
	def editPage(self, request, lessonID):
		formNewPage = FormTextPage(initial={'title': self.title, 'text': self.text})
		
		if request.POST:
			formPage = FormTextPage(request.POST)
			if formPage.is_valid():
				self.title = formPage.cleaned_data['title']
				self.text = formPage.cleaned_data['text']
				self.save()
				return HttpResponseRedirect('/lessons/edit_lesson/'+str(lessonID)+'/')
		return render_to_response('lessons/new_page.html',{'username': request.user.username,
			'lessonID':lessonID, 'form':formNewPage,
			'type': type,
			})

class FormStepPage(forms.Form):
	title = forms.CharField(max_length=200)
	text = forms.CharField(max_length = 1000, label = 'Text')
	length = forms.IntegerField()

class StepPage(models.Model):
	lesson = models.ForeignKey(Lesson)

	title = models.CharField(max_length=200)
	text = models.CharField(max_length=1000, blank = True)
	length = models.IntegerField(max_length=200)

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def getAllStep(self):
		listStep = []
		for i in self.step_set.all():
			listStep.append(i)
		for i in range(len(listStep)):
			for j in range(i, len(listStep)):
				if(listStep[i].StepNumber > listPage[j]. StepNumber):
					temp = stepPage[i]
					stepPage[i] = stepPage[j]
					stepPage[j] = temp
		return listPage

	def __unicode__(self):
		return self.title
	
class FormStep(forms.Form):
	a = forms.CharField(max_length= 1000, label = 'a')
	b = forms.CharField(max_length = 1000, label = 'b')

class Step(models.Model):
	page = models.ForeignKey(StepPage)
	a = models.CharField(max_length=1000)
	b = models.CharField(max_length=1000)

	stepNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title

