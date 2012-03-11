from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Lesson(models.Model):
	user = models.ForeignKey(User)
	lessonName = models.CharField(max_length=200)
	numberOfPape = models.IntegerField()
	def __unicode__(self):
		return self.lessonName
	
class VideoLink(models.Model):
	lesson = models.ForeignKey(User)
	link = models.CharField(max_length=200)

class ImageLink(models.Model):
	lesson = models.ForeignKey(User)
	link = models.CharField(max_length=200)

class DocumentLink(models.Model):
	lesson = models.ForeignKey(User)
	link = models.CharField(max_length=200)

class TextLink(models.Model):
	lesson = models.ForeignKey(User)
	text = models.CharField(max_length=10000)
