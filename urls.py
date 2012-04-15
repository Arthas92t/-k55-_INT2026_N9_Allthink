from django.conf.urls.defaults import patterns, include, url
import settings 
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'main.views.index'),
	
	url(r'^login/$', 'account.views.login_user'),
	url(r'^register/$','account.views.register'),
	url(r'^logout/$', 'account.views.logout_user'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^lessons/new_lesson/$', 'lessons.views.createLesson'),
	url(r'^lessons/edit_lesson/(\d+)/$', 'lessons.views.editLesson'),
	url(r'^lessons/view_lesson/(\d+)/$', 'lessons.views.viewLesson'),
	url(r'^lessons/delete_lesson/(\d+)/$', 'lessons.views.deleteLesson'),
	
	url(r'^lessons/new_page/(\d+)/([a-z]+)/$', 'lessons.views.newPage'),
	url(r'^lessons/view_page/(\d+)/(\d+)/$', 'lessons.views.viewPage'),
	url(r'^lessons/edit_page/(\d+)/(\d+)/$', 'lessons.views.editPage'),
	url(r'^lessons/delete_page/(\d+)/(\d+)/$', 'lessons.views.deletePage'),
	url(r'^lessons/up_page/(\d+)/(\d+)/$', 'lessons.views.upPage'),
	url(r'^lessons/down_page/(\d+)/(\d+)/$', 'lessons.views.downPage'),
	
	url(r'^test', 'lessons.views.test'),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'c:/django/AllThink/static/'}),
)
