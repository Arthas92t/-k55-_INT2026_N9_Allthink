from django.conf.urls.defaults import patterns, include, url
import settings 
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'main.views.home'),
	url(r'^index/$', 'main.views.index'),
	url(r'^login/$', 'account.views.login_user'),
	url(r'^register/$','account.views.register'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^logout/$', 'account.views.logout_user'),
	url(r'^lessons/new_lesson/$', 'lessons.views.createLesson'),
	url(r'^lessons/edit_lesson/(\d+)/$', 'lessons.views.editLesson'),
	url(r'^lessons/delete_lesson/(\d+)/$', 'lessons.views.deleteLesson'),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'c:/django/AllThink/static/'}),
)
