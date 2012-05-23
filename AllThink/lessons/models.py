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

SUBJECTS = (
		('', 'Select....'),
		('art', 'Art'),
		('math', 'Math'),
		('science', 'Science'),
		('physic', 'Physic'),
		('computer science', 'Computer Science'),
		('other', 'Other'),
	)
LEVELS = (
		('', 'Select....'),
		('e' , 'Elementary'),
		('h' , 'High school'),
		('c' , 'College'),
		('other', 'Other'),
		)
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
def content_file_name(instance, filename):
    return '/'.join(['content', instance.user.username, filename])
	
def checkFile(value):
	if value=="":
		return
	a = value.name.split(".")
	a = a[len(a)-1]
	if not((a == "doc")or(a == "docx")or(a == "xls")or(a == "xlsx")or(a == "pdf")or(a == "ppt")or(a == "pptx")
		or(a == "DOC")or(a == "DOCX")or(a == "XLS")or(a == "XLSX")or(a == "PDF")or(a == "PPT")or(a == "PPTX")
		):
		raise ValidationError(u'allow only doc, docx, xls, xlsx, ppt, pptx, pdf file')

class LessonForm(forms.Form):
	name = forms.CharField(max_length=200, label = 'Lesson Name')
	subject = forms.ChoiceField(label = 'Subject', widget= Select, choices = SUBJECTS)
	level = forms.ChoiceField(label = 'Level', widget= Select, choices = LEVELS)	
	information = forms.CharField(max_length=1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Information')

class Lesson(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	level = models.CharField(max_length=200)
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
	text = forms.CharField(max_length = 1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Text (Optional)', required=False)

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
	title = forms.CharField(max_length=200, label = 'Page Title')
	link = forms.CharField(max_length = 1000, label = 'Image URL')
	text = forms.CharField(max_length = 1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Text (Optional)', required=False)

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
	allFiles = {('','....'),}
	title = forms.CharField(max_length=200, label = 'Page Title')
	oldFile = forms.ChoiceField(label = 'Select Document', widget= Select, choices = allFiles, required=False)
	file = forms.FileField(label = 'or Upload New', required=False, validators = [checkFile])
	text = forms.CharField(max_length = 1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Text (Optional)', required=False)

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
	title = forms.CharField(max_length=200, label = 'Page Title')
	text = forms.CharField(max_length = 1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Text')

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
	title = forms.CharField(max_length=200, label = 'Page Title')
	text = forms.CharField(max_length = 1000, widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), label = 'Text', required=False)
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

	type = models.CharField(max_length=200)
	pageNumber = models.IntegerField(max_length=200)
	
	def __unicode__(self):
		return self.title
	def getAllStep(self):
		set = []
		for i in self.step_set.all():
			set = set + [i]
		return set
			
	def editPage(self, request):
		accept = False
		a = {'title': self.title, 'text': self.text}
		allStep = self.getAllStep()
		for i in range(len(allStep)):
			a['step'+ str(i + 1)] =  allStep[i].step
			a['explanation'+ str(i + 1)] = allStep[i].explanation
		formNewPage = FormStepPage(initial=a)
		if request.POST:
			formNewPage = FormStepPage(request.POST)
			if formNewPage.is_valid():
				self.title = formNewPage.cleaned_data['title']
				self.text = formNewPage.cleaned_data['text']
				self.save()
				for i in allStep:
					i.delete()
				for i in range(1,21):
					fieldStep = formNewPage.cleaned_data['step'+str(i)]
					fieldExplanation = formNewPage.cleaned_data['explanation'+str(i)]
					if(fieldStep)and(fieldExplanation):
						step = Step(page = self,
							step = fieldStep,
							explanation = fieldExplanation
							)
						step.save()
				self.save()
				accept = True
		return {'form':formNewPage, 'accept':accept}

class Step(models.Model):
	page = models.ForeignKey(StepPage)
	step = models.CharField(max_length= 1000, blank = True)
	explanation = models.CharField(max_length = 1000, blank = True)

class FormFile(forms.Form):
	file = forms.FileField(label = 'Upload New', required=False, validators = [checkFile])

class UserFile(models.Model):
	user = models.ForeignKey(User)

	file = models.FileField(upload_to = content_file_name)
	
	def uploadFile(self, request):
		self.user = request.user
		self.file = request.FILES['file']
		self.save()
	
	def __unicode__(self):
		return self.file.name.split('/')[len(self.file.name.split('/'))-1]