from django.conf.urls import patterns, include, url


urlpatterns = patterns('api_auth.views',
	url(r'auth_token/', 'get_auth_token'),
)
