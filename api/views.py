from models import *
from services import data_services as ds
from pprint import pprint
import json
import logging
from api_auth.models import InstrumentAuth
from api.models import DJ_Instrument

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

logger = logging.getLogger('eda5.api.views')


@ensure_csrf_cookie
def get_versions_list(request):
    logger.debug('User: {}'.format(request.user))
    auths = InstrumentAuth.objects.filter(user=request.user)
    ret = HttpResponse(content_type='application/json')
    payload = {
        'versions': ds.get_all_versions(),
        'perms': [auth.to_dict() for auth in auths]
    }
    ret.content = json.dumps(payload)
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
    quest = ds.get_specific_version(q_name, major, minor)
    logger.debug('Hi FROM GET_MAJOR_VERSON')
    try:
        perm = InstrumentAuth.objects.get(user=request.user,
                                          instrument__instrument_id=quest['instrument_id'],
                                          instrument__major_version=quest['version']['major']).to_dict()
    except InstrumentAuth.DoesNotExist:
        perm = {}
    else:
        perm = perm['permissions']

    ret.content = json.dumps({
        'questionnaire': quest,
        'perms': perm
    })
    return ret


@ensure_csrf_cookie
def get_interview_version(request):
    logger.info("Interview Hit: {}".format(request))

    ret = HttpResponse(content_type='application/json')
    q_name = request.GET.get('q')
    major = request.GET.get('major', 1)
    minor = request.GET.get('minor', 'current')
    logger.info('Interview client requesting {}: {}'.format(q_name, major))
    quest = ds.get_specific_version(q_name, major, minor)
    callback = request.GET['callback']
    ret.content = json.dumps(quest)
    ret.content = callback + '(' + json.dumps(quest) + ')'
    return ret


@ensure_csrf_cookie
def save_instrument(request, versiontype):
    body = json.loads(request.body)
    payload = body['questionnaire']
    logger.info('SAVING VERSION TYPE {}'.format(versiontype))
    try:
        perm = InstrumentAuth.objects.get(user=request.user,
                                           instrument__instrument_id=payload['instrument_id'],
                                          instrument__major_version=payload['version']['major'])
        logger.debug('permissions {}'.format(perm.to_dict()))

        logger.info("PERM: {}\nUSER: {}".format(perm, request.user.__dict__))
        if request.user.is_superuser:
            if perm is None:
                versiontype = 'major'

        else:
            if versiontype == 'minor':
                assert perm.owner or perm.write

    except (InstrumentAuth.DoesNotExist, AssertionError):
        return HttpResponse(status=403,
                            content="You can not modify a questionnaire that you do not have write access to.")

    logger.debug('INCOMING QUESTIONNIARE:\n{}'.format(body['questionnaire']))
    del payload['_id']
    eda5 = Instrument.frombson(body['questionnaire'])
    new_version = eda5.save(versiontype)

    if versiontype == 'major':
        instrument = DJ_Instrument()
        instrument.name = eda5.name
        instrument.instrument_id = eda5.instrument_id
        instrument.major_version = new_version.major
        instrument.shortname = new_version.shortname
        instrument.save()

        ia = InstrumentAuth()
        ia.instrument = instrument
        ia.user = request.user
        ia.owner = True
        ia.write = True
        ia.read = True
        ia.save()

    resp = HttpResponse(content_type='application/json')
    version = new_version.tojson()
    logger.info('SAVED VERSION {}'.format(version))
    resp.content = version
    return resp


@ensure_csrf_cookie
def delete_questionnaire_version(request, id, major, minor):
    perm = InstrumentAuth.objects.get(user=request.user,
                                      instrument__instrument_id=id,
                                      instrument__major_version=major)

    if not (perm.owner or perm.write):
        return HttpResponse(status=403,
                            content="You can not modify a questionnaire that you do not have write access to.")

    resp = HttpResponse(content_type='application/json')
    ret = ds.soft_delete_version(id, major, minor)
    logger.info("Response from db on delete op: {}".format(ret))
    resp.content = 'Deleted: {}->{}:{}'.format(id, major, minor)
    return resp
