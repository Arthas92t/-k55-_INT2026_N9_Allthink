from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/', include(admin.site.urls)),
	url(r'^register/$','account.views.register'),
)
