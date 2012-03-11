from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/', 'main.views.index'),
	url(r'^login/', 'account.views.login_user'),
	url(r'^register/$','account.views.register'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^logout/', 'account.views.logout_user'),
)
