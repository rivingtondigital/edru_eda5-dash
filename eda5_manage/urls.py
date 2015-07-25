from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eda5_manage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#	(r'', include('tokenapi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('tokenapi.urls')),
	url(r'^editor/', include('editor.urls')),
	url(r'^ajax/', include('api.urls')),
)

