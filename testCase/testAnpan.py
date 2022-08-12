import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq,getToken,jsonpath_getOne,jsonpath_getAll,isTradeTime
from config import domainCMBI,accountPool
from testData.data import codeData_activelist
from client import getQotToken

# 16:15--18:30 运行
# 1，有没有暗盘代码
# 2，搜索暗盘代码，出现两条数据
# 3，点击到个股详情，校验市场状态，校验价格，校验分时
# 4，点击交易，交易页面能看到价格，但是没五档
# 5，交易下单，会有拦截

# @unittest.skip('跳过')
@ddt.ddt
class TestAnpan(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## anpan 接口测试开始 ########## ')

	def setUp(self):
		self.pword=accountPool[self.args.env][self.args.account]
		pword=accountPool[self.args.env][self.args.account]
		self.session=getToken(self.args.account,pword,self.args.env,fromRedis=0)
		getQotToken(self.args.account,pword,self.args.env,token=self.session['token'])
		self.anpan_code='01945'

	@no_retry
	# @unittest.skip('跳过')
	def test_1_anpan_search(self):
		'''综合搜索--搜索暗盘股'''
		logging.info(f' ========== 测试开始 综合搜索--搜索暗盘股 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		url=f'{domainCMBI[self.args.env]}/search-center/public/es/v2/searchFinInfoPageByValue'
		dataJson={
			'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",
			'finFrom':'0',
			'finSize':'5',
			'infoFrom':'0',
			'infoSize':'5',
			'searchValue':self.anpan_code,
		}
		logging.info(f'请求数据: {dataJson}')
		dataCMBI=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {dataCMBI}')
		self.assertTrue(dataCMBI['success'])
		# 校验ipoData和stockData里共有两条对应数据
		ipoData=jsonpath_getAll(dataCMBI['result']['ipoData'],'stockCode')
		stockData=jsonpath_getAll(dataCMBI['result']['stockData'],'code')
		self.assertIn(self.anpan_code,ipoData)
		self.assertIn(f"E{self.anpan_code}",stockData)
		logging.info(f' ========== 测试结束 综合搜索--搜索暗盘股 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_2_anpan_snapshot(self):
		'''暗盘测试--快照'''
		logging.info(f' ========== 测试开始 暗盘测试--快照 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		path='/quote-query/qot/snapshot'
		dataJson={"marketCode":"E","stockCode":self.anpan_code}
		logging.info(f'请求聚源快照数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env,qotToken=self.args.qotToken)
		logging.info(f'聚源返回数据: {dataJY}')

		secStatus=jsonpath_getOne(dataJY,'secStatus')
		self.assertEqual(secStatus,13)# 市场状态13 连续交易中
		curPrice=jsonpath_getOne(dataJY,'curPrice','float')
		self.assertGreater(curPrice,0)#现价大于0

		logging.info(f' ========== 测试结束 暗盘测试--快照 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_3_anpan_timeShare(self):
		'''暗盘测试--分时'''
		logging.info(f' ========== 测试开始 暗盘测试--分时 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		path='/quote-query/quote/timeShare'
		dataJson={"marketCode":"E","stockCode":self.anpan_code}
		logging.info(f'请求聚源数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env)
		try:minutes=len(dataJY['result'])
		except TypeError:minutes=0
		if minutes<=0:logging.info(f'聚源返回数据: {dataJY}')
		# logging.info(f'聚源返回数据: {dataJY}')
		logging.info(f'分时个数: {minutes}')
		self.assertGreater(minutes,0)
		logging.info(f' ========== 测试结束 暗盘测试--分时 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_4_anpan_stockDealing(self):
		'''暗盘测试--交易页价格'''
		logging.info(f' ========== 测试开始 暗盘测试--交易页价格 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		global price,productNoJL,productName,purchasingPower,maxFee,brokeStockSell,holdNum,purchasingPower,stockNum,marketType,marketCode,productType,priceDiffer,currency
		url=f'{domainCMBI[self.args.env]}/gateway/order/stockDealing'
		dataJson=dict(self.session,**{"marketCode":"HK","productNo":self.anpan_code})
		logging.info(f'请求数据: {dataJson}')
		dataCMBI=postReq(0,dataJson,0,url=url)
		logging.info(f'返回数据: {dataCMBI}')
		price=jsonpath_getOne(dataCMBI,'newMarketPrice','str')
		productNoJL=jsonpath_getOne(dataCMBI,'productNoJL','str')
		productName=jsonpath_getOne(dataCMBI,'productName','str')
		purchasingPower=jsonpath_getOne(dataCMBI,'purchasingPower','str')
		maxFee=jsonpath_getOne(dataCMBI,'maxFee','str')
		brokeStockSell=jsonpath_getOne(dataCMBI,'brokeStockSell','str')
		holdNum=jsonpath_getOne(dataCMBI,'holdNum','str')
		purchasingPower=jsonpath_getOne(dataCMBI,'purchasingPower','str')
		stockNum=jsonpath_getOne(dataCMBI,'stockNum','str')
		marketType=jsonpath_getOne(dataCMBI,'marketType','str')
		marketCode=jsonpath_getOne(dataCMBI,'marketCode','str')
		productType=jsonpath_getOne(dataCMBI,'productType','str')
		priceDiffer=jsonpath_getOne(dataCMBI,'priceDiffer','str')
		currency=jsonpath_getOne(dataCMBI,'currency','str')
		self.assertGreater(float(price),0)

		logging.info(f' ========== 测试结束 暗盘测试--交易页价格 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_5_anpan_fiveLevel(self):
		'''暗盘测试--五档行情'''
		logging.info(f' ========== 测试开始 暗盘测试--五档行情 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		path='/quote-query/quote/fiveLevelQuotation'

		dataJson={
			"clickAt":int(time.time()),
			"deviceId":"zp_InterfaceTest",
			"deviceType":"python3",
			"loginAt":int(time.time()),
			"realTime":False,
			"sourceIp":"深圳南山区",
			"marketCode":"E",
			"stockCode":self.anpan_code,
			"token":self.session['token'],
			"userId":self.args.account
		}
		logging.info(f'请求聚源数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env)
		logging.info(f'聚源返回数据: {dataJY}')

		prices=jsonpath_getAll(dataJY,'price','float')
		self.assertEqual(0,sum(prices))
		logging.info(f' ========== 测试结束 暗盘测试--五档行情 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	def test_6_anpan_OrderCheck(self):
		'''暗盘测试--下单校验'''
		logging.info(f' ========== 测试开始 暗盘测试--下单校验 ========== ')
		# if not isTradeTime(time.time(),'anpan'):self.skipTest('当前不是暗盘交易时间段')
		global price,productNoJL,productName,purchasingPower,maxFee,brokeStockSell,holdNum,purchasingPower,stockNum,marketType,marketCode,productType,priceDiffer,currency
		url=f'{domainCMBI[self.args.env]}/gateway/order/stockOrderCheck'
		dataJson={
			"maxFee":maxFee,
			"brokeStockSell":brokeStockSell,
			"holdNum":holdNum,
			"newMarketPrice":price,
			"productNo":self.anpan_code,
			"purchasingPower":purchasingPower,
			"productNoJL":productNoJL,
			"stockNum":stockNum,
			"productName":productName,
			"marketType":marketType,
			"marketCode":marketCode,
			"productType":productType,
			"priceDiffer":priceDiffer,
			"currency":currency,
			"orderPrice":price,
			"orderType":"EL",
			"orderQty":100,
			"orderSide":"1",
			"orderAction":"1"
		}
		dataJson.update(self.session)
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url)
		logging.info(f'返回数据: {respJson}')
		self.assertFalse(respJson['success'])
		logging.info(f' ========== 测试结束 暗盘测试--下单校验 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_7_anpan_OrderAdd(self):
	# 	'''暗盘测试--交易下单'''
	# 	logging.info(f' ========== 测试开始 暗盘测试--交易下单 ========== ')
	# 	global price,productNoJL,productName,purchasingPower,maxFee,brokeStockSell,holdNum,purchasingPower,stockNum,marketType,marketCode,productType,priceDiffer,currency
	# 	url=f'{domainCMBI[self.args.env]}/gateway/order/stockOrderOperateAdd'
	# 	dataJson={
	# 		"maxFee":maxFee,
	# 		"brokeStockSell":brokeStockSell,
	# 		"holdNum":holdNum,
	# 		"newMarketPrice":price,
	# 		"productNo":self.anpan_code,
	# 		"purchasingPower":purchasingPower,
	# 		"productNoJL":productNoJL,
	# 		"stockNum":stockNum,
	# 		"productName":productName,
	# 		"marketType":marketType,
	# 		"marketCode":marketCode,
	# 		"productType":productType,
	# 		"priceDiffer":priceDiffer,
	# 		"currency":currency,
	# 		"orderPrice":price,
	# 		"orderType":"EL",
	# 		"orderQty":100,
	# 		"orderSide":"1",
	# 		"orderAction":"1",
	# 		"serialNum":str(time.time()).replace('.','')
	# 	}
	# 	dataJson.update(self.session)
	# 	logging.info(f'请求数据: {dataJson}')
	# 	respJson=postReq(0,dataJson,0,url=url)
	# 	logging.info(f'返回数据: {respJson}')
	# 	self.assertFalse(respJson['success'])
	# 	logging.info(f' ========== 测试结束 暗盘测试--交易下单 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## anpan 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()