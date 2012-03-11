from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login
from lessons.models import Lesson

from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	yourLessons = []
	otherLessons = []
	username = request.user.username
	for obj in Lesson.objects.all():
		if cmp(obj.user.username,username):
			otherLessons.append(obj)
		else:
			yourLessons.append(obj)
	return render_to_response('index.html',{'username': username,'yourLessons': yourLessons,'otherLessons': otherLessons})