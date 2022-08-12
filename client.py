import time,sys,struct,threading,json
from common import pbjson
from common.tools import getToken,assertCom_ws
# protoc --proto_path=./ --python_out=pb2 ./Common.proto ./Qot_Common.proto 

from pb2 import Common_pb2
from pb2 import Qot_Common_pb2
from pb2 import Qot_GetTimeShare_pb2
from pb2 import Qot_UpdateOrderBook_pb2
from pb2 import InitConnect_pb2
from pb2 import Qot_GetOrderBook_pb2
from pb2 import Qot_Sub_pb2
from pb2 import Qot_UpdateSnapshotQot_pb2
from pb2 import KeepAlive_pb2
from pb2 import Qot_GetSnapshotQot_pb2
from pb2 import Qot_UpdateBasicQot_pb2
from pb2 import Qot_GetBasicQot_pb2
###############################################################################################################
from config import *
from websocket import create_connection
import logging

class C2SProtoHeader:
	def __init__(self):
		self.protoId=0
		self.protoFormatType=0
		self.protoVersion=0
		self.packetSeqNum=0
		self.bodyLength=0
		self.bodySHA1=[]
		self.reserve=[]

def encodeData(cmd,req):
	c2s=C2SProtoHeader()
	c2s.protoId=cmd
	c2s.protoFormatType=0
	c2s.protoVersion=0
	c2s.packetSeqNum=0
	c2s.bodyLength=len(req.SerializeToString())
	c2s.bodySHA1=bytearray(b"")
	c2s.reserve=bytearray(b"")
	msgReqTemplate="!******%ss"%(len(req.SerializeToString()))
	data=struct.pack(msgReqTemplate,c2s.protoId,c2s.protoFormatType,c2s.protoVersion,c2s.packetSeqNum,c2s.bodyLength,c2s.bodySHA1,c2s.reserve,req.SerializeToString())
	return data

def parseData(data,types='response'):
	msgReqTemplate="!******"
	protoId,protoFormatType,protoVersion,packetSeqNum,bodyLength,bodySHA1,reserve=struct.unpack(msgReqTemplate,data[:42])
	if types=='response':
		if protoId==1001:
			rsp=InitConnect_pb2.Response()
		elif protoId==1004:
			rsp=KeepAlive_pb2.Response()
		elif protoId==3001:
			rsp=Qot_Sub_pb2.Response()
		elif protoId==3004:
			rsp=Qot_GetBasicQot_pb2.Response()
		elif protoId==3005:
			rsp=Qot_GetSnapshotQot_pb2.Response()
		elif protoId==3008:
			rsp=Qot_GetTimeShare_pb2.Response()
		elif protoId==3012:
			rsp=Qot_GetOrderBook_pb2.Response()
		elif protoId==3303:
			rsp=Qot_UpdateOrderBook_pb2.Response()
		elif protoId==3302:
			rsp=Qot_UpdateBasicQot_pb2.Response()
		elif protoId==3301:
			rsp=Qot_UpdateSnapshotQot_pb2.Response()
		else:
			raise Exception(f"未知的 protoId: {protoId}")
	elif types=='request':
		if protoId==1001:
			rsp=InitConnect_pb2.Request()
		elif protoId==1004:
			rsp=KeepAlive_pb2.Request()
		elif protoId==3001:
			rsp=Qot_Sub_pb2.Request()
		elif protoId==3004:
			rsp=Qot_GetBasicQot_pb2.Request()
		elif protoId==3005:
			rsp=Qot_GetSnapshotQot_pb2.Request()
		elif protoId==3008:
			rsp=Qot_GetTimeShare_pb2.Request()
		elif protoId==3012:
			rsp=Qot_GetOrderBook_pb2.Request()
		elif protoId==3303:
			rsp=Qot_UpdateOrderBook_pb2.Request()
		elif protoId==3302:
			rsp=Qot_UpdateBasicQot_pb2.Request()
		elif protoId==3301:
			rsp=Qot_UpdateSnapshotQot_pb2.Request()
		else:
			raise Exception(f"未知的 protoId: {protoId}")
	rsp.ParseFromString(data[42:])
	return protoId,rsp
	# return pbjson.pb2json(rsp)

#####################################构造不同的接口请求数据#######################################################
def init_req(userId='511703',loginToken=''):
	# ok	1001	InitConnect
	reqJson={
		'userId':userId,
		'loginToken':loginToken,
		'deviceId':"python_zp",
		'appVerCode':33558544,
		'deviceType':Common_pb2.DeviceType_Android,
		'hardware':'xiaomi',
		'systemVer':'Android6.0',
		'recvNotify':True,
		'doQotLogin':True,
		'packetEncAlgo':1,
		'pushProtoFmt':0,
	}
	c2s=pbjson.dict2pb(InitConnect_pb2.C2S,reqJson)
	req=InitConnect_pb2.Request()
	req.c2s.CopyFrom(c2s)
	return req

def sub_req(data):
	# ok	3001	Qot_Sub 订阅
	req=Qot_Sub_pb2.Request()
	c2s=Qot_Sub_pb2.C2S()
	for d in data["secuList"]:
		secu=Qot_Common_pb2.Security()
		secu.market=d["market"]
		secu.code=d["code"]
		c2s.securityList.append(secu)
	for d in data["subTypeList"]:
		c2s.subTypeList.append(d)
	for d in data["regPushRehabTypeList"]:
		c2s.regPushRehabTypeList.append(d)
	c2s.isSubOrUnSub=data["isSubOrUnSub"]
	c2s.isFirstPush=data["isFirstPush"]
	c2s.isUnsubAll=data["isUnsubAll"]
	req.c2s.CopyFrom(c2s)
	return req

def keep_req(time_int):
	# ok	1004	KeepAlive
	req=KeepAlive_pb2.Request()
	c2s=KeepAlive_pb2.C2S()
	c2s.time=int(time_int)
	req.c2s.CopyFrom(c2s)
	return req

def getBasicQot_req(market,code):
	# ok	3004	QT_GetBasicQot 基础行情
	req=Qot_GetBasicQot_pb2.Request()
	c2s=Qot_GetBasicQot_pb2.C2S()
	secu=Qot_Common_pb2.Security()
	secu.market=market
	secu.code=code
	c2s.securityList.append(secu)
	req.c2s.CopyFrom(c2s)
	return req

def getSnapshotQot_req(market,code):
	# ok	3005	Qot_GetSnapshotQot 行情快照
	req=Qot_GetSnapshotQot_pb2.Request()
	c2s=Qot_GetSnapshotQot_pb2.C2S()
	secu=Qot_Common_pb2.Security()
	secu.market=market
	secu.code=code
	c2s.securityList.append(secu)
	req.c2s.CopyFrom(c2s)
	return req

def timeShare_req(market,code):
	# ok	3008	Qot_GetTimeShare 分时
	req=Qot_GetTimeShare_pb2.Request()
	c2s=Qot_GetTimeShare_pb2.C2S()
	c2s.security.market=market
	c2s.security.code=code
	req.c2s.CopyFrom(c2s)
	return req

def getOrderBook_req(market,code):
	# ok	3012	Qot_GetOrderBook 买卖档
	req=Qot_GetOrderBook_pb2.Request()
	c2s=Qot_GetOrderBook_pb2.C2S()
	c2s.security.market=market
	c2s.security.code=code
	req.c2s.CopyFrom(c2s)
	return req

#####################################公用方法################################################################
def send_msg(wsConn,connCode,req,getRecv=0):
	binData=encodeData(connCode,req)
	wsConn.send_binary(binData)
	if getRecv:
		recv=wsConn.recv()
		code,resp=parseData(recv)
		# respjson=pbjson.pb2json(resp)
		respjson=json.loads(str(pbjson.pb2json(resp)))
		# print(time.strftime('%Y-%m-%d %X'),f'{code} 响应: {respjson}')
		return code,respjson

def getQotToken(uname,pword,env,args=None,token=None):
	wsConn=create_connection(wsHost[env])
	if args:
		if not args.qotToken:
			token=getToken(uname,pword,env,fromRedis=1)['token']
			logging.info(f'{uname} token: {token}')
			code,respjson=send_msg(wsConn,1001,init_req(uname,token),1)
			try:
				args.qotToken=respjson['s2c']['qotToken']
			except KeyError:
				raise KeyError(f'返回数据内没有 qotToken: {respjson}')
			logging.info(f'{uname} qotToken: {args.qotToken}')
	else:
		if not token:token=getToken(uname,pword,env)['token']
		code,respjson=send_msg(wsConn,1001,init_req(uname,token),1)
		qotToken=0
		try:
			qotToken=respjson['s2c']['qotToken']
		except KeyError:
			logging.info(f'获取 qotToken 失败: {respjson}')
		return qotToken
################################################################################################################
if __name__ == '__main__':
	import logging
	from HTMLReport.src.tools.log.handler_factory import HandlerFactory
	for handler in logging.getLogger().handlers:
		if not handler.get_name():
			logging.getLogger().removeHandler(handler)

	logging.getLogger().setLevel(logging.INFO)
	logging.getLogger().addHandler(HandlerFactory.get_std_out_handler())
	logging.getLogger().addHandler(HandlerFactory.get_std_err_handler())
	logging.getLogger().addHandler(HandlerFactory.get_stream_handler())
	logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('websocketTest.Log'))

	# from common.database import queryCodelist
	# allCode=queryCodelist(0,0,"SELECT market_code,stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A');")

	def recvice(wsConn,asserts=0):
		# for i in range(100):
		i=0
		while 1:
			logging.info(f"{i} 等待接收数据")
			recv=wsConn.recv()# 如果服务器没有数据返回，会一直卡在这里 多线程也无效 直至连接超时断开
			code,resp=parseData(recv)
			dataJson=json.loads(pbjson.pb2json(resp))
			if asserts:
				assertCom_ws(code,dataJson,1)
			else:
				logging.info(f"{i} 收到数据: {code} {dataJson}")
			i+=1
	#################################################################################
	def send_keep(wsConn):
		# for i in range(5):
		while 1:
			logging.info(f'keepAlive: 发送')
			send_msg(wsConn,1004,keep_req(int(time.time()/1000)))
			time.sleep(60)

	def send_sub(wsConn):
		# SubType_Snapshot_Full = 1; // 基础报价 (包含快照 + 分时 + 五档)
		# SubType_Snapshot_Basic = 2; // 基础报价简版（用于自选股）
		# SubType_OrderBook = 3; // 摆盘
		# for i in range(3):
		data={
			"secuList":[{"market":"A","code":"300760"},{"market":"B","code":"600519"}],
			# "secuList":[{"market":"A","code":"300760"},{"market":"B","code":"600519"}],
			"subTypeList":[1,2,3],
			"regPushRehabTypeList":[0],
			"isSubOrUnSub":True,
			"isFirstPush":False,
			"isUnsubAll":False
		}
		logging.info(f'send_sub 发送: {data}')
		send_msg(wsConn,3001,sub_req(data))
		# time.sleep(5)

		# data['isSubOrUnSub']=False
		# data['isUnsubAll']=True
		# logging.info(f'send_sub 发送: {data}')
		# send_msg(wsConn,3001,sub_req(data))

	def send_snapshot(wsConn,ifrecv=0):
		# codeList=[('N','BILI')]
		codeList=[('A','000858'),('B','603005'),('N','BILI')]
		for market_code in codeList:
			logging.info(f'send_snapshot: 发送 {market_code}')
			send_msg(wsConn,3005,getSnapshotQot_req(*market_code),ifrecv)

	def send_basicQot(wsConn,ifrecv=0):
		# codeList=[('N','BILI')]
		codeList=[('A','000858'),('B','603005'),('N','BILI')]
		for market_code in codeList:
			logging.info(f'send_basicQot: 发送 {market_code}')
			send_msg(wsConn,3004,getBasicQot_req(*market_code),ifrecv)

	def send_timeShare(wsConn,ifrecv=0):
		codeList=[('N','BILI')]
		for market_code in codeList:
			logging.info(f'send_timeShare: 发送 {market_code}')
			send_msg(wsConn,3008,timeShare_req(*market_code),ifrecv)
	
	def send_getOrderBook(wsConn,ifrecv=0):
		codeList=[('N','BILI')]
		for market_code in codeList:
			logging.info(f'send_getOrderBook: 发送 {market_code}')
			send_msg(wsConn,3012,getOrderBook_req(*market_code),ifrecv)

	env='test'
	from websocket import create_connection
	wsConn=create_connection(wsHost[env])
	uname,pword='******','******'
	token=getToken(uname,pword,env)['token']
	# token='E5DDB73C7F40B484CDD3945966CF6583'
	logging.info(f'InitConnect 发送数据: {uname} {token}')
	code,respjson=send_msg(wsConn,1001,init_req(uname,token),1)
	logging.info(f'{code} init响应: {respjson}')
	#################################################################################
	# send_timeShare(wsConn,1)
	# send_getOrderBook(wsConn,1)
	# send_basicQot(wsConn,1)
	# send_snapshot(wsConn,1)
	send_sub(wsConn)
	#################################################################################
	# thread_recvice=threading.Thread(target=recvice,args=(wsConn,))
	# # thread_keepAlive=threading.Thread(target=send_keep,args=(wsConn,))
	# thread_sub=threading.Thread(target=send_sub,args=(wsConn,))
	# # thread_basicQot=threading.Thread(target=send_basicQot,args=(wsConn,))
	# # thread_snapshot=threading.Thread(target=send_snapshot,args=(wsConn,))
	# # thread_timeShare=threading.Thread(target=send_timeShare,args=(wsConn,))

	# thread_list=[thread_recvice,thread_sub]
	# for t in thread_list:
	# 	t.start()

	# for t in thread_list:
	# 	t.join()
	#################################################################################

	wsConn.close()
	logging.info('关闭连接')