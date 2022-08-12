import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq
from config import domainCMBI
from testData.data_F10 import codeDataF10_A

# 1、 /hsf10/announcements  A股公告列表页
# 2、 /hsf10/brief  A股简况tab
# 3、 (不测)/hsf10/dividendMore  A股分红融资更多
# 4、 (不测)/hsf10/executiveMore  A股公司高管更多
# 5、 /hsf10/finance  A股财务tab
# 6、 (不测)/hsf10/more/finance  获取A股三大表更多
# 7、 (不测)/hsf10/more/mainBusiness  A股更多主营构成
# 8、 (不测)/hsf10/newsItem  A股新闻详情页获取
# 9、 /hsf10/newsList  A股新闻列表页
# 10、 (不测)/hsf10/report  A股研报详情页获取
# 11、 /hsf10/reportList  A股研报列表页
# 12、 (不测)/hsf10/shareHoldMore  A股股本股东更多

# @unittest.skip('跳过')
@ddt.ddt
class TestF10_A(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## A股F10 接口测试开始 ########## ')

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_A)
	def test_01_announcements(self,market_Code):
		'''A股公告列表页'''
		logging.info(f' ========== 测试开始 A股公告列表页 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hsf10/announcements'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 A股公告列表页 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_A)
	def test_02_brief(self,market_Code):
		'''A股简况tab'''
		logging.info(f' ========== 测试开始 A股简况tab ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hsf10/brief'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 A股简况tab ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_A)
	def test_05_finance(self,market_Code):
		'''A股财务tab'''
		logging.info(f' ========== 测试开始 A股财务tab ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hsf10/finance'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 A股财务tab ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_A)
	def test_09_newsList(self,market_Code):
		'''A股新闻列表页'''
		logging.info(f' ========== 测试开始 A股新闻列表页 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hsf10/newsList'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 A股新闻列表页 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_A)
	def test_11_reportList(self,market_Code):
		'''A股研报列表页'''
		logging.info(f' ========== 测试开始 A股研报列表页 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hsf10/reportList'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 A股研报列表页 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## A股F10 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()