import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase
from jsonpath import jsonpath

from common.tools import postReq,jsonpath_getOne
from config import domainJY,accountPool
from client import getQotToken
# 新市场行情 相关接口测试开始

# @unittest.skip('跳过')
@ddt.ddt
class TestNewMarket(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 新市场行情 相关接口测试开始 ########## ')

	def setUp(self):
		pword=accountPool[self.args.env][self.args.account]
		getQotToken(self.args.account,pword,self.args.env,self.args)

	# @ddt.data(*fundList)
	# @unittest.skip('跳过')
	@no_retry
	def test_01_homepageMarket(self):
		'''获取市场首页数据'''
		logging.info(f' ========== 测试开始 获取市场首页数据 ========== ')
		url=f'{domainJY[self.args.env]}/quote-query/mkt/index'
		dataJson={"market":"E"}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get',qotToken=self.args.qotToken)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])

		codes=jsonpath(respJson,'$..stockItems')
		for item in codes:
			codelist=[i['code'] for i in item]
			self.assertEqual(sorted(codelist),sorted(list(set(codelist))))# 检查同一排序中是否有重复的代码
		
		logging.info(f' ========== 测试结束 获取市场首页数据 ========== ')

	# @ddt.data(*fundList)
	# @unittest.skip('跳过')
	@no_retry
	def test_02_hotIndustryMore(self):
		'''获取市场首页热门行业更多数据'''
		logging.info(f' ========== 测试开始 获取市场首页热门行业更多数据 ========== ')
		url=f'{domainJY[self.args.env]}/quote-query/mkt/hotIndustryMore'
		dataJson={
			"count": 20,
			"marketCode": "E",
			"sortCategory": "RMHY",
			"sortField": "ZDF",
			"sortType": 1,
			"startPos": 0
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='post',qotToken=self.args.qotToken)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		
		logging.info(f' ========== 测试结束 获取市场首页热门行业更多数据 ========== ')

	# @ddt.data(*fundList)
	@no_retry
	@unittest.skip('跳过，市场二期内容')
	def test_03_hsgt(self):# 市场二期内容
		'''市场首页沪深港通页面数据'''
		logging.info(f' ========== 测试开始 市场首页沪深港通页面数据 ========== ')
		url=f'{domainJY[self.args.env]}/quote-query/mkt/hsgt'
		dataJson={"market":"E","realTime":True}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get',qotToken=self.args.qotToken)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		
		logging.info(f' ========== 测试结束 市场首页沪深港通页面数据 ========== ')


	@ddt.data(*('工用支援','103000'),('煤炭','002000'),('汽车','231000'),('建筑','602000'),('家庭电器及用品','232000'),('半导体','703000'),('银行','501000'),('黄金及贵金属','051000'),('一般金属及矿石','052000'),('专业零售','237000'),('食物饮品','251000'),('纺织及服饰','233000'),('旅游及消闲设施','234000'),('综合企业','800000'),('保险','502000'),('工用运输','102000'),('其他金融','503000'),('原材料','053000'),('医疗保健设备和服务','282000'),('公用事业','400000'))
	@no_retry
	# @unittest.skip('跳过')
	def test_03_more(self,data):
		'''获取市场首页更多数据'''
		logging.info(f' ========== 测试开始 获取 {data[0]} 市场数据 ========== ')
		url=f'{domainJY[self.args.env]}/quote-query/mkt/more'
		dataJson={
			"count": 20,
			"marketCode": "E",
			"sortCategory": "RMHY",
			"sortField": "ZDF",
			"sortType": 1,
			"startPos": 0,
			"stockCode": data[1]
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='post',qotToken=self.args.qotToken)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		codes=jsonpath(respJson,'$..stockItems')
		for item in codes:
			codelist=[i['code'] for i in item]
			self.assertEqual(sorted(codelist),sorted(list(set(codelist))))# 检查同一排序中是否有重复的代码
		logging.info(f' ========== 测试结束 获取 {data[0]} 市场数据 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 新市场行情 相关接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()
