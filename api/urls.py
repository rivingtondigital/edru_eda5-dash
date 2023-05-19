from django.conf.urls import url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [ 
	url(r'^v/list.json$', views.get_versions_list),
	url(r'^v/list_flat.json$', views.get_versions_list_flat),
	url(r'^v/fetch/current/(?P<q_name>\w+?).json$', views.get_current),
	url(r'^v/fetch/(?P<major>[0-9\.]+?)/(?P<minor>[0-9\.]+?|current)/(?P<q_name>\w+?)\.json$', views.get_major_version),
	url(r'^v/interview.json$', views.get_interview_version),
	url(r'^v/save/(?P<versiontype>(major|minor))$', views.save_instrument),
	url(r'^v/delete/(?P<id>[\d]+)/(?P<major>[\d]+)/(?P<minor>[\d]+)$', views.delete_questionnaire_version),
]
