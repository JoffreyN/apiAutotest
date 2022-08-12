# from client import parseData
# from common import pbjson
# from common.tools import saveTodatabase,formatSqlStr
# from mitmproxy import ctx
# import json,sys,time

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


logFile='proxy.log'
# with open(logFile,'w',encoding='utf-8') as file:file.write('')
# with open(r'proxySave.sql','w',encoding='utf-8') as f:f.write('')
# device_type='Android'
# app_version='3.0.1.49791'

################################################################################################################
import logging
from HTMLReport.src.tools.log.handler_factory import HandlerFactory
for handler in logging.getLogger().handlers:
	if not handler.get_name():
		logging.getLogger().removeHandler(handler)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(HandlerFactory.get_std_out_handler())
logging.getLogger().addHandler(HandlerFactory.get_std_err_handler())
logging.getLogger().addHandler(HandlerFactory.get_stream_handler())
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler(logFile))

################################################################################################################
# def websocket_message(flow):
# 	msg = flow.messages[-1]
# 	if msg.from_client:
# 		code,resp=parseData(msg.content,'request')
# 		dataJson=json.loads(pbjson.pb2json(resp))
# 		logging.info(f"websocket请求: {code} {dataJson}")
# 		created_at=time.strftime('%Y-%m-%d %X')
# 		saveSQL=f"INSERT INTO interfaceTest_data.count_websocket (created_at,device_type,app_version,req_code,req_data) VALUES ('{created_at}','{device_type}','{app_version}','{code}','{formatSqlStr(dataJson)}');\n"
# 		with open(r'proxySave.sql','a',encoding='utf-8') as f:f.write(saveSQL)
# 		# saveTodatabase(saveSQL)
# 	# else:
# 	# 	logging.info(f"websocket服务端返回: {code} {dataJson}")


def request(flow):
	method=flow.request.method
	url=flow.request.pretty_url
	# if 1==1:
	if 'cmbi' in url and rightEnd(url):
		logging.info(f'{url} {method} 请求')
		# contentType=flow.request.headers.get('Content-Type')
		# logging.info(f"contentType: {contentType}\n\n\n")
		logging.info(f"headers: {flow.request.headers}")
		# if method=='POST':
		# 	if 'multipart/form-data' in contentType and 'uploadImage' in url:
		# 		logging.info(f'{url} POST 请求数据: [已过滤图片数据]')
		# 	else:
		# 		logging.info(f'{url} POST 请求数据: {flow.request.text}')

def response(flow):
	respText=flow.response.text
	url=flow.request.pretty_url
	# if 1==1:
	if 'cmbi' in url and rightEnd(url.split('?')[0]):
		method=flow.request.method
		contentType='';reqData=None
		contentType=flow.request.headers.get('Content-Type')
		contentType_resp=flow.response.headers.get('Content-Type')
		
		if contentType==None:contentType=''
		if contentType_resp==None:contentType_resp=''
		if 'multipart/form-data' in contentType and 'uploadImage' in url:
			reqData='[已过滤图片数据]'
		else:
			reqData=flow.request.text
		
		if 'image' in contentType_resp:
			respData='[已过滤图片响应数据]'
		elif 'font/ttf' in contentType_resp:
			respData='[已过滤字体响应数据]'
		else:
			respData=flow.response.text.replace("\n","<br>")
		logging.info(f'{url} {method} 请求数据: {reqData} 响应: {respData}')


def rightEnd(url):
	_list=['.png','.jpg','.jpeg','.gif','.js','.css','.ico','.ttf']
	for i in _list:
		if url.endswith(i):
			return 0
	return 1

################################################################################################################
# mitmdump -s proxy.py --listen-port 8079

# 1、登录账号，已添加6个自选，在自选界面停留2分钟
# 2、点击市场-港股 停留2分钟

# 忽略域名
# file.roadshowing.com,img.zhitongcaijing.com,resource.cmbi.info,*.gelonghui.com,sentry.cmbi.com,lib.cmbi.info,sensor.cmbi.info,yx-api.cmbi.info,manhattan.didistatic.com