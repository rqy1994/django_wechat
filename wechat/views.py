from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from django.template import RequestContext, loader

import hashlib
import time
@csrf_exempt

def index(request):
	if request.method == 'GET':
		response = HttpResponse(checkSignature(request))
		return response
	else:
		#return HttpResponse('Hello World')
		xml_str = smart_str(request.body)
		#request_xml = etree.fromstring(xml_str)
		response_xml = ET.fromstring(xml_str)

		content=response_xml.find("Content").text
		msgType=response_xml.find("MsgType").text
		fromUser=response_xml.find("FromUserName").text
		toUser=response_xml.find("ToUserName").text

		template = loader.get_template('wechat/reply_text.xml')
		#return render.reply_text(fromUser,toUser,int(time.time()),content)
		#c = RequestContext({'toUser': toUser, 'fromUser': fromUser, 
		#				'nowtime': int(time.time()), 'content': content})

		#test turing rebot
		content = turing(content,fromUser)
		c = {
				'toUser': fromUser, 
				'fromUser': toUser, 
				'nowtime': str(int(time.time())), 
				'content': content
		}

		return render(request,'wechat/reply_text.xml',c)
		#return HttpResponse(template.render(c))
	

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

import requests
def turing(ask,uid):
	url = 'http://www.tuling123.com/openapi/api'
	data = {
		'key':'ab88d67fd5d83167de20708dff40de5b',
		'info':ask,
		'userid':uid
	}
	s = requests.session()
	return s.post(url = url,data = data).text[23:-2]
	

	
