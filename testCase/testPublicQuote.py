import time,logging,traceback,unittest,hashlib
from HTMLReport import ddt,no_retry

from common.parameter import ParameTestCase
from common.tools import postReq,genCodeData,jsonpath_getOne,jsonpath_getAll
from testData.data import codeData_US_list
from config import marketCodeDic

# @unittest.skip('跳过')
@ddt.ddt
class TestPublicQuote(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 大众版行情 接口开始 ########## ')
		# 只支持美股正股

	def setUp(self):
		pass

	######################################################################################################################
	# @unittest.skip('跳过')
	@no_retry
	def test_1_webQuoteAuth(self):
		'''登录和权限'''
		logging.info(f' ========== 测试开始 登录和权限 ========== ')
		global quoteToken,operatorNo
		path='/auth-center/public/quoteAuth/webQuoteAuth'
		signStr=f'krRVT8JPNvE58FBm{self.args.account}'
		dataJson={
			"traceLogId":f"FromZP{time.strftime('%Y%m%d%H%M%S')}",
			"accountNo":self.args.account,
			"sourceIp":"192.168.31.80",
			"signature":hashlib.md5(signStr.encode(encoding='UTF-8')).hexdigest().upper(),
			"loginAt":int(time.time()*1000)
		}
		logging.info(f'请求数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env)
		try:
			self.assertTrue(dataJY['success'])
		except AssertionError:
			logging.info(f'返回数据: {dataJY}')
			raise AssertionError('断言失败')
		quoteToken=jsonpath_getOne(dataJY,'quoteToken','str')
		operatorNo=jsonpath_getOne(dataJY,'operatorNo','str')
		logging.info(f' ========== 测试结束 登录和权限 ========== ')

	@no_retry
	@ddt.data(*codeData_US_list)
	# @unittest.skip('跳过')
	def test_2_snapTimeshareOrderbook(self,codeData):
		'''快照、分时、一档接口'''
		logging.info(f' ========== 测试开始 {codeData[1]}_{codeData[2]} 快照、分时、一档接口 ========== ')
		global quoteToken,operatorNo
		path='/quote-query/pop/snapTimeshareOrderbook'
		
		dataJson={
			"marketAndCode":f"{marketCodeDic[codeData[3]]}{codeData[1]}",
			"loginEvent":{
				"userId":operatorNo,
				"sourceIp":"192.168.31.80",
				"deviceId":"deviceId_PythonZP",
				"deviceType":"DeviceType_PythonZP",
				"loginAt":int(time.time()*1000)
			}
		}
		logging.info(f'请求数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env,qotToken=quoteToken,headerTraceLog=f"FromZP{time.strftime('%Y%m%d%H%M%S')}")
		try:
			self.assertTrue(dataJY['success'])
		
			curPrice=jsonpath_getOne(dataJY,'curPrice')
			buy=jsonpath_getOne(dataJY,'buy','dict')
			sell=jsonpath_getOne(dataJY,'sell','dict')
			priceList=jsonpath_getAll(dataJY,'price')
			lastClosePriceList=jsonpath_getAll(dataJY,'lastClosePrice')

			self.assertIsNotNone(curPrice)
			self.assertIsNotNone(buy)
			self.assertIsNotNone(sell)
			self.assertNotIn(None,priceList)
			self.assertNotIn(None,lastClosePriceList)
		except AssertionError:
			logging.info(f'返回数据: {dataJY}')
			raise AssertionError('断言失败')

		logging.info(f' ========== 测试结束 {codeData[1]}_{codeData[2]} 快照、分时、一档接口 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_3_simpleSnapshots(self):
		'''简版快照list接口'''
		logging.info(f' ========== 测试开始 简版快照list接口 ========== ')
		global quoteToken,operatorNo
		path='/quote-query/pop/simpleSnapshots'

		dataJson={
			"marketAndCodes": [f"{marketCodeDic[codeData[3]]}{codeData[1]}" for codeData in codeData_US_list],
			"loginEvent": {
				"userId": "operatorNo",
				"sourceIp": "192.168.31.80",
				"deviceId":"deviceId_PythonZP",
				"deviceType":"DeviceType_PythonZP",
				"loginAt": int(time.time()*1000)
			}
		}
		logging.info(f'请求数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env,qotToken=quoteToken,headerTraceLog=f"FromZP{time.strftime('%Y%m%d%H%M%S')}")
		try:
			self.assertTrue(dataJY['success'])

			xjList=jsonpath_getAll(dataJY,'xj')
			self.assertNotIn(None,xjList)
		except AssertionError:
			logging.info(f'返回数据: {dataJY}')
			raise AssertionError('断言失败')

		logging.info(f' ========== 测试结束 简版快照list接口 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 大众版行情 接口结束 ########## ')

if __name__=='__main__':
	unittest.main()