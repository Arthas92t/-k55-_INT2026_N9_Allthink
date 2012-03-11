from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

def login_user(request):
	return HttpResponseRedirect('/login/')
	state = "Please login below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		if user is not None:
				login(request, user)
				return HttpResponseRedirect('/admin/')
		else:
			state = "Your username and/or password were incorrect."
			
	return render_to_response('login.html',{'state':state, 'username': username})