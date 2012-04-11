from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
# Create your models here.

class Lesson(models.Model):
	user = models.ForeignKey(User)
	lessonName = models.CharField(max_length=200)
	information = models.CharField(max_length=1000)
	
	def __unicode__(self):
		return self.lessonName
	
	def addPage(self, form, type):
		if type == 'video':
			newPage = VideoPage()
			newPage.link = form.cleaned_data['link']
		if type == 'image':
			newPage = ImagePage()
			newPage.link = form.cleaned_data['link']
		if type == 'document':
			newPage = DocumentPage()
			newPage.link = form.cleaned_data['link']
		if type == 'text':
			newPage = TextPage()
			
		newPage.lesson = self
		newPage.title = form.cleaned_data['title']
		newPage.text = form.cleaned_data['text']
		newPage.type = type
		newPage.pageNumber = self.len()
		
		newPage.save()
		self.save()

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
		for i in range(len(listPage)):
			for j in range(i, len(listPage)):
				if(listPage[i].pageNumber > listPage[j]. pageNumber):
					temp = listPage[i]
					listPage[i] = listPage[j]
					listPage[j] = temp
		return listPage
	
	def len(self):
		len = 0
		len = len + self.videopage_set.count()
		len = len + self.imagepage_set.count()
		len = len + self.documentpage_set.count()
		len = len + self.textpage_set.count()
		return len
		
	def getPage(self, number):
		for i in self.videopage_set.all():
			if i.pageNumber == int(number):
				return i
		for i in self.imagepage_set.all():
			if i.pageNumber == int(number):
				return i
		for i in self.documentpage_set.all():
			if i.pageNumber == int(number):
				return i
		for i in self.textpage_set.all():
			if i.pageNumber == int(number):
				return i
	
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
