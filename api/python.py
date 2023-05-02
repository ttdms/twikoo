from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import parse_qs
# -*- coding: utf8 -*-


class handler(BaseHTTPRequestHandler):


    def do_GET(self):
        def getTocken(id, secert, msg, agentId):
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + \
                id + "&corpsecret=" + secert

            r = requests.get(url)
            tocken_json = json.loads(r.text)
            # print(tocken_json['access_token'])
            sendText(tocken=tocken_json['access_token'], agentId=agentId, msg=msg)

        def sendText(tocken, agentId, msg):
            sendUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + tocken
            # print(sendUrl)
            data = json.dumps({
                "safe": 0,
                "touser": "@all",
                "msgtype": "text",
                "agentid": agentId,
                "text": {
                    "content": str(msg)
                }
            })
            requests.post(sendUrl, data)

        try:
            params = parse_qs(self.path[12:])
            apiid = params['id'][0]
            apisecert = params['secert'][0]
            apiagentId = params['agentId'][0]
            apimsg = params['msg'][0]
        except:
            apimsg = self.path
        else:
            #try:
            # 执行主程序
            getTocken(id=apiid, secert=apisecert,
                        msg=apimsg, agentId=apiagentId)
            #except:
            #    status = 1
            #    apimsg = '主程序运行时出现错误，请检查参数是否填写正确。详情可以参阅：https://blog.zhheo.com/p/1e9f35bc.html'
            #else:
            #    status = 0
        # print(event)
        # print("Received event: " + json.dumps(event, indent = 2))
        # print("Received context: " + str(context))
        # print("Hello world")

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(apimsg)
        return
