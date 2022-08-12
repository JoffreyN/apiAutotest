import time,logging,traceback,unittest,json
from HTMLReport import ddt,no_retry

from common.parameter import ParameTestCase
from common.tools import genCodeData,getToken,assertCom_ws
from client import send_msg,sub_req,init_req,timeShare_req,getSnapshotQot_req,getOrderBook_req
from testData.data import codeData_activelist
from config import *
# @unittest.skip('跳过')
@ddt.ddt
class TestWebsocket(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## websocket接口测试开始 ########## ')

	def setUp(self):
		pass

	def test_1_INIT_CONNECT(self):
		'''初始化连接'''
		logging.info(f' ========== 测试开始 1001 INIT_CONNECT ========== ')
		
		pword=accountPool[self.args.env][self.args.account]
		loginToken=getToken(self.args.account,pword,self.args.env,self.args.getTokenFromRedis)['token']
		logging.info(f'INIT_CONNECT 发送: {self.args.account} {loginToken}')
		code,respJson=send_msg(self.wsConn,1001,init_req(self.args.account,loginToken),1)
		logging.info(f'{code} INIT_CONNECT 返回数据: {respJson}')
		try:
			self.args.qotToken=respJson['s2c']['qotToken']
		except:
			pass
		assertCom_ws(code,respJson)
		logging.info(f' ========== 测试结束 1001 INIT_CONNECT ========== ')

	@no_retry
	# @unittest.skip('跳过')
	# @ddt.data(*genCodeData())
	@ddt.data(*codeData_activelist)
	def test_2_ws_GetSnapshotQot(self,codeData):
		'''行情快照'''
		logging.info(f' ========== 测试开始 3005 Qot_GetSnapshotQot ========== ')
		if self.args.skipWarrants:
			if codeData[0] in ['HKN','HKX','HKZ','HKG']:
				self.skipTest('跳过涡轮代码')
		if codeData[3]==303 and codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 没有美股指数权限')
		logging.info(f"Qot_GetSnapshotQot 发送: {marketCodeDic[codeData[3]]} {codeData[1]}")
		code,respJson=send_msg(self.wsConn,3005,getSnapshotQot_req(marketCodeDic[codeData[3]],codeData[1]),1)
		logging.info(f'{code} Qot_GetSnapshotQot 返回数据: {respJson}')
		assertCom_ws(code,respJson)
		logging.info(f' ========== 测试结束 3005 Qot_GetSnapshotQot ========== ')

	# @ddt.data(('E','00700'),('A','000858'),('B','603005'),('N','BILI'))
	# @ddt.data(('E','00700'),('A','000858'),('B','603005'))
	@no_retry
	# @unittest.skip('跳过')
	# @ddt.data(*genCodeData())
	@ddt.data(*codeData_activelist)
	def test_3_ws_GetTimeShare(self,codeData):
		'''分时数据'''
		logging.info(f' ========== 测试开始 3008 Qot_GetTimeShare ========== ')
		if self.args.skipWarrants:
			if codeData[0] in ['HKN','HKX','HKZ','HKG']:
				self.skipTest('跳过涡轮代码')
		if codeData[3]==303 and codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 没有美股指数权限')
		logging.info(f'Qot_GetTimeShare 发送数据: {marketCodeDic[codeData[3]]} {codeData[1]}')
		code,respJson=send_msg(self.wsConn,3008,timeShare_req(marketCodeDic[codeData[3]],codeData[1]),1)
		logging.info(f'{code} Qot_GetTimeShare 返回数据: {respJson}')
		assertCom_ws(code,respJson)
		logging.info(f' ========== 测试结束 3008 Qot_GetTimeShare ========== ')

	# @unittest.skip('跳过')
	@no_retry
	# @ddt.data(*genCodeData())
	@ddt.data(*codeData_activelist)
	def test_4_ws_GetOrderBook(self,codeData):
		'''买卖档'''
		logging.info(f' ========== 测试开始 3012 Qot_GetOrderBook ========== ')
		if self.args.skipWarrants:
			if codeData[0] in ['HKN','HKX','HKZ','HKG']:
				self.skipTest('跳过涡轮代码')
		if codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 指数没有买卖档')
		logging.info(f"Qot_GetOrderBook 发送数据: {marketCodeDic[codeData[3]]} {codeData[1]}")
		code,respJson=send_msg(self.wsConn,3012,getOrderBook_req(marketCodeDic[codeData[3]],codeData[1]),1)
		logging.info(f'{code} Qot_GetOrderBook 返回数据: {respJson}')
		assertCom_ws(code,respJson)
		logging.info(f' ========== 测试结束 3012 Qot_GetOrderBook ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# @ddt.data(('E','00700'),('A','000858'),('B','603005'))
	# # @ddt.data(('E','00700'),('A','000858'),('B','603005'),('N','BILI'))
	# def test_2_QT_SUB(self,stockList):
	# 	'''订阅 遍历字段subTypeList'''
	# 	logging.info(f' ========== 测试开始 QT_SUB ========== ')
	# 	dataJson={
	# 		"secuList":[{"market":stockList[0],"code":stockList[1]}],
	# 		"subTypeList":[1],
	# 		"regPushRehabTypeList":[],
	# 		"isSubOrUnSub":True,
	# 		"isFirstPush":True,
	# 		"isUnsubAll":False
	# 	}
	# 	logging.info(f'QT_SUB 发送数据: {dataJson}')
	# 	code,respJson=send_msg(self.wsConn,3001,sub_req(dataJson),1)
	# 	logging.info(f'{code} QT_SUB 返回数据: {respJson}')
	# 	assertCom_ws(code,respJson)
	# 	logging.info(f' ========== 测试结束 QT_SUB ========== ')
	
	# # @unittest.skip('跳过')
	# # @no_retry
	# @ddt.data((False,False,False),(False,False,True),(False,True,False),(False,True,True),(True,False,False),(True,False,True),(True,True,False),(True,True,True))
	# @ddt.unpack
	# def test_2__QT_SUB(self,a,b,c):
	# 	'''订阅 遍历isSubOrUnSub、isFirstPush、isUnsubAll三个字段排列组合'''
	# 	logging.info(f' ========== 测试开始 QT_SUB ========== ')
	# 	dataJson={
	# 		"secuList":[{"market":"E","code":"00700"}],
	# 		"subTypeList":[1],
	# 		"regPushRehabTypeList":[],
	# 		"isSubOrUnSub":a,
	# 		"isFirstPush":b,
	# 		"isUnsubAll":c
	# 	}
	# 	logging.info(f'QT_SUB 发送数据: {dataJson}')
	# 	code,respJson=send_msg(self.wsConn,3001,sub_req(dataJson),1)
	# 	logging.info(f'{code} QT_SUB 返回数据: {respJson}')
	# 	logging.info(f' ========== 测试结束 QT_SUB ========== ')


	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## websocket接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()