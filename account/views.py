# Create your views here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission

from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def get_user(username):
	try:
		return User.objects.get(username=username)
	except User.DoesNotExist:
		return None
		
def register(request):
	state = "fill all field below"
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = get_user(username)
		if user is None:
			user = User.objects.create_user(username,'',password)
			permission = Permission.objects.get(codename="add_lesson")
			user.user_permissions.add(permission)
			user.is_staff = True
			user.save()
			return HttpResponseRedirect('/admin/')
		else:
			state = 'This username has already exist'
	return render_to_response('register.html',{'state':state, 'username': username})