from django.conf.urls import url

from . import views

urlpatterns = [ 
	url(r'auth_token/', views.get_auth_token),
]
