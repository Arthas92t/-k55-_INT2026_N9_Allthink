from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Lesson(models.Model):
	user = models.ForeignKey(User)
	lessonName = models.CharField(max_length=200)
	pageList = []
	
	def __unicode__(self):
		return self.lessonName
	
class VideoPage(models.Model):
	title = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	def __init(self):
		self.nextPage = None
	def __unicode__(self):
		return self.title

class ImagePage(models.Model):
	title = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	def __init(self):
		self.nextPage = None
	def __unicode__(self):
		return self.title

class DocumentPage(models.Model):
	title = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	def __init(self):
		self.nextPage = None
	def __unicode__(self):
		return self.title

class TextPage(models.Model):
	title = models.CharField(max_length=200)
	text = models.CharField(max_length=10000)
	def __init(self):
		self.nextPage = None
	def __unicode__(self):
		return self.title
