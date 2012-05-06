from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.forms.widgets import *
import os

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
# Create your models here.

def lessonPermission(request, lesson):
	return request.user == lesson.user
	
def pagePermission(request, page):
	return request.user == page.lesson.user

def get_lesson(lessonID = 0, name =''):
	if cmp(name,'') != 0:
		try:              
			return Lesson.objects.get(name=name)
		except Lesson.DoesNotExist:
			return None
	try:
		return Lesson.objects.get(pk=lessonID)
	except Lesson.DoesNotExist:
		return None

def get_file(fileID = 0):
	try:
		return UserFile.objects.get(pk=fileID)
	except UserFile.DoesNotExist:
		return None

class Lesson(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=200)
	information = models.CharField(max_length=1000)
	userJoined = models.ManyToManyField(User, related_name='lessonsjoined')

	def __unicode__(self):
		return self.name
	
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
			newPage.length = 0

		newPage.lesson = self
		newPage.type = type
		newPage.pageNumber = self.len()
		return newPage.editPage(request)
		
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
		allPage = self.getAllPage()
		if int(number) < len(allPage):
			return allPage[int(number)]
		return None
	
class FormVideoPage(forms.Form):
	title = forms.CharField(max_length=200, required = True)
	link = forms.CharField(max_length = 1000, label = 'Video URL', required = True)
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

	def editPage(self, request):
		formNewPage = FormVideoPage(initial={'title': self.title, 'link': self.link, 'text': self.text})
		accept = False
		if request.POST:
			formNewPage = FormVideoPage(request.POST)
			if formNewPage.is_valid():
				self.link = formNewPage.cleaned_data['link']
				self.title = formNewPage.cleaned_data['title']
				self.text = formNewPage.cleaned_data['text']
				self.save()
				accept = True
		return {'form':formNewPage, 'accept':accept}

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

	def editPage(self, request):
		formNewPage = FormImagePage(initial={'title': self.title, 'link': self.link, 'text': self.text})
		accept = False
		if request.POST:
			formNewPage = FormImagePage(request.POST)
			if formNewPage.is_valid():
				if not (type == 'text'):
					self.link = formNewPage.cleaned_data['link']
				self.title = formNewPage.cleaned_data['title']
				self.text = formNewPage.cleaned_data['text']
				self.save()
				accept = True
		return {'form':formNewPage, 'accept':accept}

class FormDocumentPage(forms.Form):
	allFiles = {('','....')}
	title = forms.CharField(max_length=200)
	oldFile = forms.ChoiceField(label = 'Select Document', widget= Select, choices = allFiles, required=False)
	file = forms.FileField(label = 'or Upload New', required=False)
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

	def editPage(self, request):
		accept = False
		allFiles = ((None,'-----'),)
		for i in request.user.userfile_set.all():
			allFiles = allFiles + ((i.file.url ,i),)
		formNewPage = FormDocumentPage(initial={'title': self.title, 'text': self.text})
		formNewPage.fields['oldFile'].choices = allFiles
		formNewPage.fields['oldFile'].initial = self.link
		if request.POST:
			formNewPage = FormDocumentPage(request.POST, request.FILES)
			allFiles = ((None,'-----'),)
			for i in request.user.userfile_set.all():
				allFiles = allFiles + ((i.file.url ,i.file.name),)
			formNewPage.fields['oldFile'].choices = allFiles
			if formNewPage.is_valid():
				if (formNewPage.fields['oldFile']) or (formNewPage.fields['file']):
					self.link = formNewPage.cleaned_data['oldFile']
					if request.FILES:
						file = UserFile()
						file.uploadFile(request)
						self.link = file.file.url
						file.save()
					self.title = formNewPage.cleaned_data['title']
					self.text = formNewPage.cleaned_data['text']
					self.save()
					accept = True
		return {'form':formNewPage, 'accept':accept}

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
	def editPage(self, request):
		accept = False
		formNewPage = FormTextPage(initial={'title': self.title, 'text': self.text})
		
		if request.POST:
			formNewPage = FormTextPage(request.POST)
			if formNewPage.is_valid():
				self.title = formNewPage.cleaned_data['title']
				self.text = formNewPage.cleaned_data['text']
				self.save()
				accept = True
		return {'form':formNewPage, 'accept':accept}

class FormStepPage(forms.Form):
	title = forms.CharField(max_length=200)
	text = forms.CharField(max_length = 1000, label = 'Text', required=False)
	step1 = forms.CharField(max_length= 1000, label = 'Step1', required=False)
	explanation1 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step2 = forms.CharField(max_length= 1000, label = 'Step2', required=False)
	explanation2 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step3 = forms.CharField(max_length= 1000, label = 'Step3', required=False)
	explanation3 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step4 = forms.CharField(max_length= 1000, label = 'Step4', required=False)
	explanation4 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step5 = forms.CharField(max_length= 1000, label = 'Step5', required=False)
	explanation5 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step6 = forms.CharField(max_length= 1000, label = 'Step6', required=False)
	explanation6 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step7 = forms.CharField(max_length= 1000, label = 'Step7', required=False)
	explanation7 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step8 = forms.CharField(max_length= 1000, label = 'Step8', required=False)
	explanation8 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step9 = forms.CharField(max_length= 1000, label = 'Step9', required=False)
	explanation9 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step10 = forms.CharField(max_length= 1000, label = 'Step10', required=False)
	explanation10 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step11 = forms.CharField(max_length= 1000, label = 'Step11', required=False)
	explanation11 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step12 = forms.CharField(max_length= 1000, label = 'Step12', required=False)
	explanation12 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step13 = forms.CharField(max_length= 1000, label = 'Step13', required=False)
	explanation13 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step14 = forms.CharField(max_length= 1000, label = 'Step14', required=False)
	explanation14 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step15 = forms.CharField(max_length= 1000, label = 'Step15', required=False)
	explanation15 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step16 = forms.CharField(max_length= 1000, label = 'Step16', required=False)
	explanation16 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step17 = forms.CharField(max_length= 1000, label = 'Step17', required=False)
	explanation17 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step18 = forms.CharField(max_length= 1000, label = 'Step18', required=False)
	explanation18 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step19 = forms.CharField(max_length= 1000, label = 'Step19', required=False)
	explanation19 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)
	step20 = forms.CharField(max_length= 1000, label = 'Step20', required=False)
	explanation20 = forms.CharField(max_length = 1000, label = 'Explanation', required=False)

class StepPage(models.Model):
	lesson = models.ForeignKey(Lesson)

	title = models.CharField(max_length=200)
	text = models.CharField(max_length=1000, blank = True)
	step1 = models.CharField(max_length= 1000, blank = True)
	explanation1 = models.CharField(max_length = 1000, blank = True)
	step2 = models.CharField(max_length= 1000, blank = True)
	explanation2 = models.CharField(max_length = 1000, blank = True)
	step3 = models.CharField(max_length= 1000, blank = True)
	explanation3 = models.CharField(max_length = 1000, blank = True)
	step4 = models.CharField(max_length= 1000, blank = True)
	explanation4 = models.CharField(max_length = 1000, blank = True)
	step5 = models.CharField(max_length= 1000, blank = True)
	explanation5 = models.CharField(max_length = 1000, blank = True)
	step6 = models.CharField(max_length= 1000, blank = True)
	explanation6 = models.CharField(max_length = 1000, blank = True)
	step7 = models.CharField(max_length= 1000, blank = True)
	explanation7 = models.CharField(max_length = 1000, blank = True)
	step8 = models.CharField(max_length= 1000, blank = True)
	explanation8 = models.CharField(max_length = 1000, blank = True)
	step9 = models.CharField(max_length= 1000, blank = True)
	explanation9 = models.CharField(max_length = 1000, blank = True)
	step10 = models.CharField(max_length= 1000, blank = True)
	explanation10 = models.CharField(max_length = 1000, blank = True)
	step11 = models.CharField(max_length= 1000, blank = True)
	explanation11 = models.CharField(max_length = 1000, blank = True)
	step12 = models.CharField(max_length= 1000, blank = True)
	explanation12 = models.CharField(max_length = 1000, blank = True)
	step13 = models.CharField(max_length= 1000, blank = True)
	explanation13 = models.CharField(max_length = 1000, blank = True)
	step14 = models.CharField(max_length= 1000, blank = True)
	explanation14 = models.CharField(max_length = 1000, blank = True)
	step15 = models.CharField(max_length= 1000, blank = True)
	explanation15 = models.CharField(max_length = 1000, blank = True)
	step16 = models.CharField(max_length= 1000, blank = True)
	explanation16 = models.CharField(max_length = 1000, blank = True)
	step17 = models.CharField(max_length= 1000, blank = True)
	explanation17 = models.CharField(max_length = 1000, blank = True)
	step18 = models.CharField(max_length= 1000, blank = True)
	explanation18 = models.CharField(max_length = 1000, blank = True)
	step19 = models.CharField(max_length= 1000, blank = True)
	explanation19 = models.CharField(max_length = 1000, blank = True)
	step20 = models.CharField(max_length= 1000, blank = True)
	explanation20 = models.CharField(max_length = 1000, blank = True)

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title
	def getAllStep(self):
		allStep = []
		allExp = []
		if(self.step1 and self.explanation1):
			allStep = allStep + [self.step1]
			allExp = allExp + [self.explanation1]
		if(self.step2 and self.explanation2):
			allStep = allStep + [self.step2]
			allExp = allExp + [self.explanation2]
		if(self.step3 and self.explanation3):
			allStep = allStep + [self.step3]
			allExp = allExp + [self.explanation3]
		if(self.step4 and self.explanation4):
			allStep = allStep + [self.step4]
			allExp = allExp + [self.explanation4]
		if(self.step5 and self.explanation5):
			allStep = allStep + [self.step5]
			allExp = allExp + [self.explanation5]
		if(self.step6 and self.explanation6):
			allStep = allStep + [self.step6]
			allExp = allExp + [self.explanation6]
		if(self.step7 and self.explanation7):
			allStep = allStep + [self.step7]
			allExp = allExp + [self.explanation7]
		if(self.step8 and self.explanation8):
			allStep = allStep + [self.step8]
			allExp = allExp + [self.explanation8]
		if(self.step9 and self.explanation9):
			allStep = allStep + [self.step9]
			allExp = allExp + [self.explanation9]
		if(self.step10 and self.explanation10):
			allStep = allStep + [self.step10]
			allExp = allExp + [self.explanation10]
		if(self.step11 and self.explanation11):
			allStep = allStep + [self.step11]
			allExp = allExp + [self.explanation11]
		if(self.step12 and self.explanation12):
			allStep = allStep + [self.step12]
			allExp = allExp + [self.explanation12]
		if(self.step13 and self.explanation13):
			allStep = allStep + [self.step13]
			allExp = allExp + [self.explanation13]
		if(self.step14 and self.explanation14):
			allStep = allStep + [self.step14]
			allExp = allExp + [self.explanation14]
		if(self.step15 and self.explanation15):
			allStep = allStep + [self.step15]
			allExp = allExp + [self.explanation15]
		if(self.step16 and self.explanation16):
			allStep = allStep + [self.step16]
			allExp = allExp + [self.explanation16]
		if(self.step17 and self.explanation17):
			allStep = allStep + [self.step17]
			allExp = allExp + [self.explanation17]
		if(self.step18 and self.explanation18):
			allStep = allStep + [self.step18]
			allExp = allExp + [self.explanation18]
		if(self.step19 and self.explanation19):
			allStep = allStep + [self.step19]
			allExp = allExp + [self.explanation19]
		if(self.step20 and self.explanation20):
			allStep = allStep + [self.step20]
			allExp = allExp + [self.explanation20]
		return allStep, allExp
			
	def editPage(self, request):
		accept = False
		a = {'title': self.title, 'text': self.text}
		allStep, allExp = self.getAllStep()
		for i in range(len(allStep)):
			a['step'+ str(i + 1)] =  allStep[i]
			a['explanation'+ str(i + 1)] = allExp[i]
		formNewPage = FormStepPage(initial=a)
		if request.POST:
			formNewPage = FormStepPage(request.POST)
			if formNewPage.is_valid():
				self.title = formNewPage.cleaned_data['title']
				self.text = formNewPage.cleaned_data['text']
				self.step1 = formNewPage.cleaned_data['step1']
				self.step2 = formNewPage.cleaned_data['step2']
				self.step3 = formNewPage.cleaned_data['step3']
				self.step4 = formNewPage.cleaned_data['step4']
				self.step5 = formNewPage.cleaned_data['step5']
				self.step6 = formNewPage.cleaned_data['step6']
				self.step7 = formNewPage.cleaned_data['step7']
				self.step8 = formNewPage.cleaned_data['step8']
				self.step9 = formNewPage.cleaned_data['step9']
				self.step10 = formNewPage.cleaned_data['step10']
				self.step11 = formNewPage.cleaned_data['step11']
				self.step12 = formNewPage.cleaned_data['step12']
				self.step13 = formNewPage.cleaned_data['step13']
				self.step14 = formNewPage.cleaned_data['step14']
				self.step15 = formNewPage.cleaned_data['step15']
				self.step16 = formNewPage.cleaned_data['step16']
				self.step17 = formNewPage.cleaned_data['step17']
				self.step18 = formNewPage.cleaned_data['step18']
				self.step19 = formNewPage.cleaned_data['step19']
				self.step20 = formNewPage.cleaned_data['step20']
				self.explanation1 = formNewPage.cleaned_data['explanation1']
				self.explanation2 = formNewPage.cleaned_data['explanation2']
				self.explanation3 = formNewPage.cleaned_data['explanation3']
				self.explanation4 = formNewPage.cleaned_data['explanation4']
				self.explanation5 = formNewPage.cleaned_data['explanation5']
				self.explanation6 = formNewPage.cleaned_data['explanation6']
				self.explanation7 = formNewPage.cleaned_data['explanation7']
				self.explanation8 = formNewPage.cleaned_data['explanation8']
				self.explanation9 = formNewPage.cleaned_data['explanation9']
				self.explanation10 = formNewPage.cleaned_data['explanation10']
				self.explanation11 = formNewPage.cleaned_data['explanation11']
				self.explanation12 = formNewPage.cleaned_data['explanation12']
				self.explanation13 = formNewPage.cleaned_data['explanation13']
				self.explanation14 = formNewPage.cleaned_data['explanation14']
				self.explanation15 = formNewPage.cleaned_data['explanation15']
				self.explanation16 = formNewPage.cleaned_data['explanation16']
				self.explanation17 = formNewPage.cleaned_data['explanation17']
				self.explanation18 = formNewPage.cleaned_data['explanation18']
				self.explanation19 = formNewPage.cleaned_data['explanation19']
				self.explanation20 = formNewPage.cleaned_data['explanation20']
				self.save()
				accept = True
		return {'form':formNewPage, 'accept':accept}
	
class FormFile(forms.Form):
	file = forms.FileField(label = 'Upload New', required=False)

class UserFile(models.Model):
	user = models.ForeignKey(User)

	file = models.FileField(upload_to = 'file')
	
	def uploadFile(self, request):
		self.user = request.user
		self.file = request.FILES['file']
		self.save()
	
	def __unicode__(self):
		return self.file.name.split('/')[len(self.file.name.split('/'))-1]