from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^api/admin/', include(admin.site.urls)),
    url(r'^api/auth/', include('api_auth.urls')),
    url(r'^api/editor/', include('editor.urls')),
    url(r'^api/ajax/', include('api.urls')),
    # url(r'', include('tokenapi.urls')),
]
