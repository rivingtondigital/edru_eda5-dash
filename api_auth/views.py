from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError

# Create your views here.

def get_auth_token(request):
	print 'got token request'
	ret = HttpResponse(content_type='application/json')
	ret.content = 'recieved'
	return ret