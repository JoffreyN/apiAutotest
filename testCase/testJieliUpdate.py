import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq
from config import domainCMBI,marketCodeDic
from testData.data import codeData_activelist

# @unittest.skip('跳过')
@ddt.ddt
class TestJLupdate(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 捷力升级 接口测试开始 ########## ')

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeData_activelist)
	def test_01_realTime(self,codeData):
		'''分时数据'''
		logging.info(f' ========== 测试开始 分时数据 ========== ')
		secuCode=f"{marketCodeDic[codeData[3]]}{codeData[1]}"
		path='/gateway2/stock/realTime'
		dataJson={'code':secuCode,'traceLogId':f"FromZP{str(time.time()).replace('.','')}"}
		logging.info(f'请求数据: {dataJson}')
		respJson_test=postReq(0,dataJson,0,url=f'{domainCMBI["test"]}{path}')
		logging.info(f'TEST 返回数据: {respJson_test}')
		respJson_prod=postReq(0,dataJson,0,url=f'{domainCMBI["prod"]}{path}')
		logging.info(f'PROD 返回数据: {respJson_prod}')
		self.assertEqual(respJson_test,respJson_prod)
		# try:
		# 	self.assertEqual(respJson_test,respJson_prod)
		# except AssertionError:
		# 	logging.info(f'TEST 返回数据: {respJson_test}\nPROD 返回数据: {respJson_prod}\n断言失败:',exc_info=True)
		logging.info(f' ========== 测试结束 分时数据 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeData_activelist)
	def test_02_orderbook(self,codeData):
		'''买卖档行情'''
		logging.info(f' ========== 测试开始 买卖档行情 ========== ')
		secuCode=f"{marketCodeDic[codeData[3]]}{codeData[1]}"
		path='/gateway2/stock/orderbook'
		dataJson={'code':secuCode,'traceLogId':f"FromZP{str(time.time()).replace('.','')}"}
		logging.info(f'请求数据: {dataJson}')
		respJson_test=postReq(0,dataJson,0,url=f'{domainCMBI["test"]}{path}')
		logging.info(f'TEST 返回数据: {respJson_test}')
		respJson_prod=postReq(0,dataJson,0,url=f'{domainCMBI["prod"]}{path}')
		logging.info(f'PROD 返回数据: {respJson_prod}')
		self.assertEqual(respJson_test,respJson_prod)
		# try:
		# 	self.assertEqual(respJson_test,respJson_prod)
		# except AssertionError:
		# 	logging.info(f'TEST 返回数据: {respJson_test}\nPROD 返回数据: {respJson_prod}\n断言失败:',exc_info=True)
		logging.info(f' ========== 测试结束 买卖档行情 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeData_activelist)
	def test_03_quote(self,codeData):
		'''行情快照'''
		logging.info(f' ========== 测试开始 行情快照 ========== ')
		secuCode=f"{marketCodeDic[codeData[3]]}{codeData[1]}"
		path='/gateway2/stock/quote'
		dataJson={'code':secuCode,'traceLogId':f"FromZP{str(time.time()).replace('.','')}"}
		logging.info(f'请求数据: {dataJson}')
		respJson_test=postReq(0,dataJson,0,url=f'{domainCMBI["test"]}{path}')
		logging.info(f'TEST 返回数据: {respJson_test}')
		respJson_prod=postReq(0,dataJson,0,url=f'{domainCMBI["prod"]}{path}')
		logging.info(f'PROD 返回数据: {respJson_prod}')
		self.assertEqual(respJson_test,respJson_prod)
		# try:
		# 	self.assertEqual(respJson_test,respJson_prod)
		# except AssertionError:
		# 	logging.info(f'TEST 返回数据: {respJson_test}\nPROD 返回数据: {respJson_prod}\n断言失败:',exc_info=True)
		logging.info(f' ========== 测试结束 行情快照 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	# @ddt.data(*codeData_activelist)
	def test_04_stockpicks(self):
		'''查询自选股票详情'''
		logging.info(f' ========== 测试开始 查询自选股票详情 ========== ')
		path='/gateway2/stock/stockpicks'
		dataJson={'traceLogId':f"FromZP{str(time.time()).replace('.','')}",'list':['A399001','B1A0001','A399300','E01249','E00700','E00513','E08030','E08356','E08613','A300760','B600519']}
		logging.info(f'请求数据: {dataJson}')
		respJson_test=postReq(0,dataJson,0,url=f'{domainCMBI["test"]}{path}')
		logging.info(f'TEST 返回数据: {respJson_test}')
		respJson_prod=postReq(0,dataJson,0,url=f'{domainCMBI["prod"]}{path}')
		logging.info(f'PROD 返回数据: {respJson_prod}')
		self.assertEqual(respJson_test,respJson_prod)
		# try:
		# 	self.assertEqual(respJson_test,respJson_prod)
		# except AssertionError:
		# 	logging.info(f'TEST 返回数据: {respJson_test}\nPROD 返回数据: {respJson_prod}\n断言失败:',exc_info=True)
		logging.info(f' ========== 测试结束 查询自选股票详情 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 捷力升级 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()