from models import *
from services import data_services as ds
from pprint import pprint
import json
import logging


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

logger = logging.getLogger('eda5.api.views')


@ensure_csrf_cookie
def get_versions_list(request):
        logger.debug('calling get_version_list')        
	ret = HttpResponse(content_type='application/json')
	# callback = request.GET['callback']
	versions = ds.get_all_versions()
	ret.content = json.dumps(versions)
	# ret.content = callback+'('+ json.dumps(versions) +')'
	return ret

@ensure_csrf_cookie
def get_versions_list_flat(request):
	ret = HttpResponse(content_type='application/json')
	# callback = request.GET['callback']
	versions = ds.get_all_versions_flat()
	ret.content = json.dumps(versions)
	# ret.content = callback+'('+ json.dumps(versions) +')'
	return ret


@ensure_csrf_cookie
def get_current(request, q_name):
	ret = HttpResponse(content_type='application/json')
	quest = ds.get_current_questionnaire(q_name)
	# callback = request.GET['callback']
	ret.content = json.dumps(quest)
	# ret.content = callback+'('+json.dumps(quest)+')'
	return ret


@ensure_csrf_cookie
def get_major_version(request, major, minor, q_name):
	ret = HttpResponse(content_type='application/json')
	print major, q_name
	quest = ds.get_specific_version(q_name, major, minor)
	ret.content = json.dumps(quest)
	return ret

@ensure_csrf_cookie
def get_interview_version(request):
	ret = HttpResponse(content_type='application/json')
	q_name = request.GET.get('q')
	major = request.GET.get('major', 1)
	minor = request.GET.get('minor', 'current')
	logger.debug('Interview client requesting {}: {}'.format(q_name, major))
	quest = ds.get_specific_version(q_name, major, minor)
	callback = request.GET['callback']
	ret.content = json.dumps(quest)
	ret.content = callback+'('+ json.dumps(quest) +')'
	return ret


@ensure_csrf_cookie
def save_instrument(request, versiontype):
	body = json.loads(request.body)
	logger.info('INCOMING QUESTIONNIARE:\n{}'.format(body['questionnaire']))
	payload = body['questionnaire']
	del payload['_id']
	eda5 = Instrument.frombson(body['questionnaire'])
	new_version = eda5.save(versiontype)
	resp = HttpResponse(content_type='application/json')
	version = new_version.tojson()
	logger.info('SAVED VERSION {}'.format(version))
	resp.content = version
	return resp


@ensure_csrf_cookie
def delete_questionnaire_version(request, instrument_id):
	resp = HttpResponse(content_type='application/json')
	ds.soft_delete_version(instrument_id)
	print 'Deleted this: ', instrument_id
	resp.content = 'Deleted: ', instrument_id
	return resp
