from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('api.views',
    url(r'^v/list.json$', 'get_versions_list'),
    url(r'^v/list_flat.json$', 'get_versions_list_flat'),
    url(r'^v/fetch/current/(?P<q_name>\w+?).json$', 'get_current'),
    url(r'^v/fetch/(?P<major>[0-9\.]+?)/(?P<minor>[0-9\.]+?|current)/(?P<q_name>\w+?)\.json$', 'get_major_version'),
    url(r'^v/interview.json$', 'get_interview_version'),
    url(r'^v/save/(?P<versiontype>(major|minor))$', 'save_instrument'),
    url(r'^v/delete/(?P<instrument_id>[\w\d]+)$', 'delete_questionnaire_version'),
    url(r'^v/new_questionnaire', 'new_questionnaire'),
)
