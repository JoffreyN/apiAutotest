import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq
from config import domainCMBI
from testData.data_F10 import codeDataF10_HK

# 1、 (不测)/hkf10/announcement  获取港股公告详情
# 2、 /hkf10/announcements  获取港股F10公告列表
# 3、 /hkf10/brief  获取港股简况tab数据
# 4、 (不测)/hkf10/brief/more/dividend  获取更多分红派息
# 5、 (不测)/hkf10/brief/more/holdSharesChange  获取更多持股变动
# 6、 (不测)/hkf10/brief/more/leaderPosition  获取更多公司高管
# 7、 (不测)/hkf10/brief/more/shareholder  获取更多股本股东
# 8、 (不测)/hkf10/detail  股票百科详情信息
# 9、 /hkf10/finance  获取港股财务tab数据
# 10、 (不测)/hkf10/more/finance  获取港股三大表更多
# 11、 (不测)/hkf10/more/mainBusiness  获取港股主营构成更多
# 12、 /hkf10/myAnnouncements  获取自选股公告列表
# 13、 (不测)/hkf10/newsItem  获取港股新闻详情
# 14、 /hkf10/newsList  获取港股新闻列表
# 15、 /hkf10/sellShort  获取港股做空成交比例及更多

# @unittest.skip('跳过')
@ddt.ddt
class TestF10_HK(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 港股F10 接口测试开始 ########## ')

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_02_announcements(self,market_Code):
		'''获取港股F10公告列表'''
		logging.info(f' ========== 测试开始 获取港股F10公告列表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/announcements'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取港股F10公告列表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_03_brief(self,market_Code):
		'''获取港股简况tab数据'''
		logging.info(f' ========== 测试开始 获取港股简况tab数据 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/brief'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取港股简况tab数据 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_09_finance(self,market_Code):
		'''获取港股财务tab数据'''
		logging.info(f' ========== 测试开始 获取港股财务tab数据 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/finance'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取港股财务tab数据 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_12_myAnnouncements(self,market_Code):
		'''获取自选股公告列表'''
		logging.info(f' ========== 测试开始 获取自选股公告列表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/myAnnouncements'
		dataJson={'marketAndCodes':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取自选股公告列表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_14_newsList(self,market_Code):
		'''获取港股新闻列表'''
		logging.info(f' ========== 测试开始 获取港股新闻列表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/newsList'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取港股新闻列表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataF10_HK)
	def test_15_sellShort(self,market_Code):
		'''获取港股做空成交比例及更多'''
		logging.info(f' ========== 测试开始 获取港股做空成交比例及更多 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/hkf10/sellShort'
		dataJson={'marketAndCode':market_Code}
		logging.info(f'请求数据: {dataJson}')

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		logging.info(f'返回数据: {respJson}')
		logging.info(f'耗时: {_spendTime}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取港股做空成交比例及更多 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 港股F10 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()