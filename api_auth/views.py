from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.models import User
import logging
import json
from api_auth.models import AuthToken
from datetime import datetime

# Create your views here.
logger = logging.getLogger('eda5.dashboard.auth.views')

def get_auth_token(request):
    try:
        logger.info(request.body)
        payload = json.loads(request.body)
        username = payload.get('username')
        password = payload.get('password')
        assert username and password
        user = User.objects.get(username=username)
        assert user.check_password(password)

    except (User.DoesNotExist, AssertionError):
        return HttpResponse("Username/password does not match any user in our system.", status=400)
    except:
        logger.error('Could not decode payload', exc_info=True)
        raise

    try:
        logger.info('Requesting Token for {}'.format(user.email))
        token = AuthToken()
        token.ip_address = request.META['REMOTE_ADDR']
        token.user = user
        token.issued = token.renewed = datetime.now()
        hash = token.get_token()
        logger.debug('Token for {} is {}'.format(user.id, hash))
        token.save()


        ret = HttpResponse(content_type='application/json')
        ret.content = hash
    except:
        logger.error('Could not return token', exc_info=True)
        raise

    return ret