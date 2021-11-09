# -*- coding: utf-8 -*-
import hashlib
from WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
from flask import Flask,request,abort
from flask import jsonify,render_template
from medicine import eat,need_to_eat,is_today_eaten,fake_date
import settings

import time
import json
import datetime

# #文本回复xml格式模板
# TEXT_REPLAY = '''
#     <xml>
#         <ToUserName><![CDATA[%s]]></ToUserName>
#         <FromUserName><![CDATA[%s]]></FromUserName>
#         <CreateTime>%s</CreateTime>
#         <MsgType><![CDATA[%s]]></MsgType>
#         <Content><![CDATA[%s]]></Content>
#     </xml>
#         '''
# #图片回复xml模板
# IMAGE_REPLAY = '''
#     <xml>
#         <ToUserName><![CDATA[%s]]></ToUserName>
#         <FromUserName><![CDATA[%s]]></FromUserName>
#         <CreateTime>%s</CreateTime>
#         <MsgType><![CDATA[%s]]></MsgType>
#         <Image>
#             <MediaId><![CDATA[%s]]></MediaId>
#         </Image>
#         </xml>
#     '''
app = Flask(__name__)

#/wechat表示网络文件夹全部路径为 
#http://你的ip地址/wechat 即可实现访问
@app.route("/wechat",methods =['GET','POST'])
def wechat():
    try:
        signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        
        if not all([signature,timestamp,nonce]):
            abort(400)

        wxcpt=WXBizMsgCrypt(settings.sToken,settings.sEncodingAESKey,settings.WECOM_CID)
        if request.method == "GET":
                ret,sEchoStr=wxcpt.VerifyURL(signature, timestamp,nonce,echostr)
                if(ret!=0):
                    print ("ERR: VerifyURL ret: " + str(ret))
                    return "error"
                else:
                    return sEchoStr
                
        elif request.method == "POST":
            ret,sMsg=wxcpt.DecryptMsg( request.data, signature, timestamp, nonce)
            if( ret!=0 ):
                print ("ERR: DecryptMsg ret: " + str(ret))
                return "error"
            else:
                try:
                    #用request接收发送来的xml消息
                    
                    print(sMsg)
                    xmldata = sMsg.decode('utf-8')
                    #处理xml数据
                    xml_rec = ET.fromstring(xmldata)
                    #获取相关参数
                    ToUserName = xml_rec.find('ToUserName').text
                    FromUserName = xml_rec.find('FromUserName').text
                    CreateTime = xml_rec.find('CreateTime').text
                    Content = xml_rec.find('Content').text
                    MsgId = xml_rec.find('MsgId').text
                    AgentID = xml_rec.find('AgentID').text
                    print(xmldata)

                    if Content == "吃了":
                        today = fake_date(datetime.datetime.now())
                        if not need_to_eat(today):
                            sRespData = f"<xml><ToUserName>{FromUserName}</ToUserName><FromUserName>{ToUserName}</FromUserName><CreateTime>{CreateTime}</CreateTime><MsgType>text</MsgType><Content>今天不用吃药</Content><MsgId>{MsgId}</MsgId><AgentID>1000002</AgentID></xml>"
                            ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, nonce, timestamp)
                            if( ret!=0 ):
                                print ("ERR: EncryptMsg ret: " + str(ret))
                                return "error"
                            else:
                                return sEncryptMsg
                        else:
                            if is_today_eaten(today):
                                sRespData = f"<xml><ToUserName>{FromUserName}</ToUserName><FromUserName>{ToUserName}</FromUserName><CreateTime>{CreateTime}</CreateTime><MsgType>text</MsgType><Content>今天已经吃药了</Content><MsgId>{MsgId}</MsgId><AgentID>1000002</AgentID></xml>"
                                ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, nonce, timestamp)
                                if( ret!=0 ):
                                    print ("ERR: EncryptMsg ret: " + str(ret))
                                    return "error"
                                else:
                                    return sEncryptMsg
                            else:
                                eat(today)
                                sRespData = f"<xml><ToUserName>{FromUserName}</ToUserName><FromUserName>{ToUserName}</FromUserName><CreateTime>{CreateTime}</CreateTime><MsgType>text</MsgType><Content>吃药成功</Content><MsgId>{MsgId}</MsgId><AgentID>1000002</AgentID></xml>"
                                ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, nonce, timestamp)
                                if( ret!=0 ):
                                    print ("ERR: EncryptMsg ret: " + str(ret))
                                    return "error"
                                else:
                                    return sEncryptMsg
                    else:
                        sRespData = f"<xml><ToUserName>{FromUserName}</ToUserName><FromUserName>{ToUserName}</FromUserName><CreateTime>{CreateTime}</CreateTime><MsgType>text</MsgType><Content>听不懂/:pig言/:pig语</Content><MsgId>{MsgId}</MsgId><AgentID>1000002</AgentID></xml>"
                        ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, nonce, timestamp)
                        if( ret!=0 ):
                            print ("ERR: EncryptMsg ret: " + str(ret))
                            return "error"
                        else:
                            return sEncryptMsg
                except Exception as e:
                    raise e   
    except Exception as e:
        raise e

@app.route("/hello",methods =['GET','POST'])
def hello():
    return "hello"

if __name__ == '__main__':
    app.run("127.0.0.1",port=8080, debug =False)



