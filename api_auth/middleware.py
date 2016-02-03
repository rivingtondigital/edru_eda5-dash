
import logging
import re
from django.http import HttpResponse
from api_auth.models import AuthToken
from django.conf import settings
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger('eda5.dashboard.auth.middleware')

class WebTokenMiddleware(object):

    def unauthed(self):
        response = HttpResponse("""<html><title>Auth required</title><body>
                                <h1>Authorization Required</h1></body></html>""", mimetype="text/json")
        response.status_code = 401
        return response

    def process_request(self, request):
#        logger.debug('{} Requesting {}'.format(request.user, request.path))
        if request.path == '/api/auth/auth_token/':
            return None
        if request.path == '/api/ajax/v/interview.json':
            return None
        if '/api/admin' in request.path:
            return None

        try:
            meta = request.META
            logger.debug('AuthToken: {}'.format(meta.get('HTTP_AUTHTOKEN', 'None')))
#            logger.debug('{}'.format('\n'.join(["{} -> {}".format(m, meta[m]) for m in meta])))
            token = meta.get('HTTP_AUTHTOKEN')
            ip_addy = meta.get('REMOTE_ADDR')
            token_obj = AuthToken.objects.get(token=token)
            logger.debug(token_obj)
            assert token, 'Token not found'
            assert token_obj.ip_address == ip_addy, 'Token does not match ip address on record. {}: {}'.format(
                token_obj.ip_address,
                ip_addy
            )
            time_since = timezone.now() - token_obj.renewed
            logger.debug('Time since last refresh: {}. Limit {}'.format(time_since.total_seconds() / 60, settings.TIMEOUT))
            assert (time_since.total_seconds() / 60) < settings.TIMEOUT, 'Token expired'
            token_obj.renewed = datetime.now()
            token_obj.save()
        except (AuthToken.DoesNotExist, AssertionError) as e:
            logger.info('Auth Failed {}'.format(str(e)))
            return HttpResponse(status=401)
        except:
            logger.error('Failed to process auth request', exc_info=True)
            raise
        logger.info('Successful Authentication for {}'.format(token_obj.user.username))
        request.user = token_obj.user

        return None

    def process_response(self, request, response):
        response['Auth_Timeout'] = settings.TIMEOUT
        return response

