from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Lesson(models.Model):
	user = models.ForeignKey(User)
	lessonsName = models.CharField(max_length=200)
	
	def add_lesson(request):
		a = 1

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
