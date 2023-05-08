from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [ 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('api_auth.urls')),
    url(r'^editor/', include('editor.urls')),
    url(r'^ajax/', include('api.urls')),
    # url(r'', include('tokenapi.urls')),
]
