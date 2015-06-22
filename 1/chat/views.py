#coding=utf-8
import hashlib
import json
from xml.etree import ElementTree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime


def checkSignature(request):
    TOKEN = 'hxsoccer123'
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    token = TOKEN
    tmpList = [token,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return HttpResponse(echoStr)
    else:
        return HttpResponse("ERROR")

def parseTxtMsg(request):
    xmlstr = smart_str(request.body)
    xml =ElementTree.fromstring(xmlstr)
    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime =xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text
    Content = xml.find('Content').text
    MsgId = xml.find('MsgId').text
    if Content == '1':
        msg = '悬崖边上放了一个 WARNING 的牌子，结果只有程序猿掉了下去...'
    elif Content == '2':
        msg = datetime.datetime.now()
    else:
        msg = '欢迎访问虎溪联队微信公众号，本公众号正在建设中，目前提供的服务有限，输入1听一个笑话，输入2查看当前时间,任意输入将重新收到本消息。'
    return sendTxtMsg(FromUserName,ToUserName,msg)


def sendTxtMsg(FromUserName,ToUserName,Content):
    reply_xml = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>""" %(FromUserName,ToUserName,datetime.datetime.now(),Content)

    return HttpResponse(reply_xml)

@csrf_exempt
def weixin(request):
    if request.method == 'GET':
        return checkSignature(request)
    else:
        return parseTxtMsg(request)
