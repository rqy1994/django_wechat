from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import hashlib

@csrf_exempt

def index(request):
	if request.method == 'GET':
		response = HttpResponse(checkSignature(request))
		return response
	else:
		#return HttpResponse('Hello World')
	

def checkSignature(request):
	signature=request.GET.get('signature',)
	timestamp=request.GET.get('timestamp',None)
	nonce=request.GET.get('nonce',None)
	echostr=request.GET.get('echostr',None)
	token='renqingyu2'

	tmplist = [token,timestamp,nonce]
	tmplist.sort()
	tmpstr = "%s%s%s"%tuple(tmplist)
	tmpstr = hashlib.sha1(tmpstr).hexdigest()
	if tmpstr == signature:
		return echostr
	else:
		return None
