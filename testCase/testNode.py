import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq,getToken,jsonpath_getOne,jsonpath_getAll
from config import domainCMBI,marketCodeDic,accountPool
from testData.data import codeData_activelist

# /gateway2/stock/stockInfo		F10查询港A指数成分股股票信息
# /gateway/order/stockOrderCheck		港碎A下单校验
# /gateway/order/stockSelHoldQuery	持仓查询
# /gateway/order/ordersQuery		订单查询
# /gateway/order/findFinanceRate		可融股票查询
# /gateway2/appMe/selectAppMutilRecord	app热门板块查询列表
# /gateway2/appMe/selectAppModelDetail	app热门板块查询详细
# /ifpt/app/article/news		资讯服务
# /search-center/public/es/v2/searchFinInfoPageByValue	综合搜索

# @unittest.skip('跳过')
@ddt.ddt
class TestNode(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## node 接口测试开始 ########## ')

	def setUp(self):
		self.pword=accountPool[self.args.env][self.args.account]

	# # @unittest.skip('跳过')
	# @no_retry
	# @ddt.data(*codeData_activelist)
	# def test_01_02_stockInfo(self,codeData):
	# 	'''查询港A指数成分股或判断正股类型'''
	# 	logging.info(f' ========== 测试开始 查询港A指数成分股或判断正股类型 ========== ')
	# 	if codeData[3]==303 and codeData[0]=='zhishu':self.skipTest('美股不支持成分股，跳过')
	# 	url=f'{domainCMBI[self.args.env]}/gateway2/stock/stockInfo'
	# 	secuCode=f"{marketCodeDic[codeData[3]]}{codeData[1]}"
	# 	# A股票；I指数；N牛熊证；W认证股
	# 	types='I' if codeData[0]=='zhishu' else "A"
	# 	dataJson={
	# 		"secuCode":secuCode,
	# 		"type":types,
	# 		"traceLogId":f"FromZP{time.strftime('%Y%m%d%H%M%S')}",
	# 		"pageNo":10
	# 	}
	# 	logging.info(f'请求数据: {dataJson}')
	# 	dataCMBI=postReq(0,dataJson,0,url=url)
	# 	logging.info(f'返回数据: {dataCMBI}')
	# 	self.assertTrue(dataCMBI['success'])
	# 	# 股票信息 股票类型
	# 	if types=="I":
	# 		stocks=len(dataCMBI['result']['data'][0]['data'])
	# 		logging.info(f'{secuCode} 成分股个数: {stocks}')
	# 		self.assertGreater(stocks,0)
	# 	logging.info(f' ========== 测试结束 查询港A指数成分股或判断正股类型 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	@ddt.data('港股','碎股','A股')
	def test_03_04_stockOrderCheck(self,types):
		'''港碎A下单校验'''
		logging.info(f' ========== 测试开始 港碎A下单校验 ========== ')
		url=f'{domainCMBI[self.args.env]}/gateway/order/stockOrderCheck'
		session=getToken('511703','aaaa1111',self.args.env,self.args.getTokenFromRedis)
		if types=='A股':
			dataJson={
				"maxFee":"210870.00","brokeStockSell":"0","holdNum":"0","purchasingPower":"100000000.000","productNoJL":"B600036","newMarketPrice":"42.750","stockNum":100,"productNo":"600036","productName":"招商银行","marketType":"SH","marketCode":"SHA","productType":"A","priceDiffer":"0.01","currency":"CNY","orderType":"PL","orderPrice":"42.750","orderQty":100,"orderSide":"1","orderAction":"1"
			}
		elif types=='碎股':
			dataJson={
				"maxFee":"307629.79","brokeStockSell":"99","holdNum":"50099","purchasingPower":"99944677.450","productNoJL":"E02018","newMarketPrice":"44.600","stockNum":"500","productNo":"02018","productName":"瑞声科技","marketType":"HK","marketCode":"HK","productType":"A","priceDiffer":"0.05","currency":"HKD","orderType":"BS","orderPrice":"44.600","orderQty":1,"orderSide":"2","orderAction":"1"
			}
		elif types=='港股':
			dataJson={
				"maxFee":"307800.00","brokeStockSell":"0","holdNum":"0","purchasingPower":"100000000.000","productNoJL":"E00700","newMarketPrice":"625.000","stockNum":"100","productNo":"00700","productName":"腾讯控股","marketType":"HK","marketCode":"HK","productType":"A","priceDiffer":"0.5","currency":"HKD","orderType":"EL","orderPrice":"625.000","orderQty":100,"orderSide":"1","orderAction":"1"
			}
		dataJson.update(session)
		logging.info(f'请求数据: {dataJson}')
		for i in range(5):
			respJson=postReq(0,dataJson,0,url=url)
			logging.info(f'返回数据: {respJson}')
			try:
				if '网络异常' not in respJson['errorMsg']:break
			except TypeError:
				break
		flag=1 if respJson['errorMsg']==None or '请在交易日' in respJson['errorMsg'] else 0
		self.assertTrue(flag)
		# 单手股数
		# stockNum=respJson['result']['stockNum'
		# logging.info(f'每手股数: {stockNum}')]
		logging.info(f' ========== 测试结束 港碎A下单校验 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	@ddt.data('港股','碎股','A股')
	def test_05_stockOrderOperateAdd(self,types):
		'''港碎A下单'''
		logging.info(f' ========== 测试开始 港碎A下单 ========== ')
		url=f'{domainCMBI[self.args.env]}/gateway/order/stockOrderOperateAdd'
		session=getToken('511703','aaaa1111',self.args.env,self.args.getTokenFromRedis)
		if types=='A股':
			dataJson={
				"maxFee":"210870.00","brokeStockSell":"0","holdNum":"0","purchasingPower":"100000000.000","productNoJL":"B600036",
				"newMarketPrice":"42.750","stockNum":100,"productNo":"600036","productName":"招商银行","marketType":"SH","marketCode":"SHA",
				"productType":"A","priceDiffer":"0.01","currency":"CNY","orderType":"PL","orderPrice":"42.750","orderQty":100,"orderSide":"1",
				"orderAction":"1","serialNum":str(time.time()).replace('.','')
			}
		elif types=='碎股':
			dataJson={
				"maxFee":"307629.79","brokeStockSell":"99","holdNum":"50099","purchasingPower":"99944677.450","productNoJL":"E02018",
				"newMarketPrice":"44.600","stockNum":"500","productNo":"02018","productName":"瑞声科技","marketType":"HK","marketCode":"HK",
				"productType":"A","priceDiffer":"0.05","currency":"HKD","orderType":"BS","orderPrice":"44.600","orderQty":1,"orderSide":"2",
				"orderAction":"1","serialNum":str(time.time()).replace('.','')
			}
		elif types=='港股':
			dataJson={
				"maxFee":"307800.00","brokeStockSell":"0","holdNum":"0","purchasingPower":"100000000.000","productNoJL":"E00700",
				"newMarketPrice":"625.000","stockNum":"100","productNo":"00700","productName":"腾讯控股","marketType":"HK","marketCode":"HK",
				"productType":"A","priceDiffer":"0.5","currency":"HKD","orderType":"EL","orderPrice":"625.000","orderQty":100,"orderSide":"1",
				"orderAction":"1","serialNum":str(time.time()).replace('.','')
			}
		dataJson.update(session)
		logging.info(f'请求数据: {dataJson}')
		for i in range(5):
			respJson=postReq(0,dataJson,0,url=url)
			logging.info(f'返回数据: {respJson}')
			try:
				if '网络异常' not in respJson['errorMsg']:break
			except TypeError:
				break
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 港碎A下单 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_06_01_stockSelHoldQuery(self):
	# 	'''持仓查询'''
	# 	logging.info(f' ========== 测试开始 持仓查询 ========== ')
	# 	url=f'{domainCMBI[self.args.env]}/gateway/order/stockSelHoldQuery'
	# 	session=getToken('511703','aaaa1111',self.args.env,self.args.getTokenFromRedis)
	# 	logging.info(f'请求数据: {session}')
	# 	respJson=postReq(0,session,0,url=url)
	# 	logging.info(f'返回数据: {respJson}')
	# 	self.assertTrue(respJson['success'])
	# 	# 名称、现价
	# 	logging.info(f' ========== 测试结束 持仓查询 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	def test_06_01_queryAccountAndHold(self):
		'''用于客户查询股票持仓和账户资产数据'''
		logging.info(f' ========== 测试开始 持仓查询 ========== ')
		url=f'{domainCMBI[self.args.env]}/gateway/order/queryAccountAndHold'
		session=getToken('511703','aaaa1111',self.args.env,self.args.getTokenFromRedis)
		logging.info(f'请求数据: {session}')
		respJson=postReq(0,session,0,url=url)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		# 名称、现价
		logging.info(f' ========== 测试结束 持仓查询 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	def test_07_ordersQuery(self):
		'''订单查询'''
		logging.info(f' ========== 测试开始 订单查询 ========== ')
		url=f'{domainCMBI[self.args.env]}/gateway/order/ordersQuery'
		session=getToken('511703','aaaa1111',self.args.env,self.args.getTokenFromRedis)
		dataJson={"limit":20,"page":1,"traceLogId":f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
		dataJson.update(session)
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		# 名称
		logging.info(f' ========== 测试结束 订单查询 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*(['HK','E02338'],['HK','E02359'],['HK',''],['US','']))
	def test_08_findFinanceRate(self,codeData):
		'''可融股票查询'''
		logging.info(f' ========== 测试开始 可融股票查询 ========== ')
		url=f'{domainCMBI[self.args.env]}/gateway/order/findFinanceRate'
		if codeData[1]:
			dataJson={"marketType":codeData[0],"productNo":codeData[1],"traceLogId":f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
		else:
			dataJson={"marketType":codeData[0],"traceLogId":f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url)
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		productNameList=jsonpath_getAll(respJson,'productName')
		newPriceList=jsonpath_getAll(respJson,'newPrice')
		zdfList=jsonpath_getAll(respJson,'zdf')
		zdList=jsonpath_getAll(respJson,'zd')
		# 名称，现价，涨跌幅，涨跌额
		self.assertNotIn(None,productNameList)
		self.assertNotIn(None,newPriceList)
		self.assertNotIn(None,zdfList)
		self.assertNotIn(None,zdList)
		logging.info(f' ========== 测试结束 可融股票查询 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# @ddt.data('HK','US')
	# def test_09_1_selectAppMutilRecord(self,mtype):
	# 	'''app热门板块查询列表'''
	# 	logging.info(f' ========== 测试开始 app热门板块查询列表 ========== ')
	# 	url=f'{domainCMBI[self.args.env]}/gateway2/appMe/selectAppMutilRecord'
	# 	dataJson={"isAppFirst":'NO',"marketType":mtype}
	# 	logging.info(f'请求数据: {dataJson}')
	# 	respJson=postReq(0,dataJson,0,url=url)
	# 	logging.info(f'返回数据: {respJson}')
	# 	self.assertTrue(respJson['success'])
	# 	# 名称，现价，涨跌幅，涨跌额
	# 	logging.info(f' ========== 测试结束 app热门板块查询列表 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# @ddt.data('港股特色十九','港股特色二十一','美股特色五','美股特色十')
	# def test_09_2_selectAppModelDetail(self,modelName):
	# 	'''app热门板块查询详细'''
	# 	logging.info(f' ========== 测试开始 app热门板块查询详细 ========== ')
	# 	url=f'{domainCMBI[self.args.env]}/gateway2/appMe/selectAppModelDetail'
	# 	dataJson={"modelName":modelName,"sortByType":'desc'}
	# 	logging.info(f'请求数据: {dataJson}')
	# 	respJson=postReq(0,dataJson,0,url=url)
	# 	logging.info(f'返回数据: {respJson}')
	# 	self.assertTrue(respJson['success'])
	# 	# 名称，现价，涨跌幅，涨跌额
	# 	logging.info(f' ========== 测试结束 app热门板块查询详细 ========== ')

	@no_retry
	@ddt.data(1504193,1501538,1499778)
	# @unittest.skip('跳过')
	def test_09_article(self,articleId):
		'''资讯服务'''
		logging.info(f' ========== 测试开始 资讯服务 ========== ')

		url=f'{domainCMBI[self.args.env]}/ifpt/app/article/news'
		dataJson={'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",'articleId':articleId}
		logging.info(f'请求数据: {dataJson}')
		dataCMBI=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {dataCMBI}')
		self.assertTrue(dataCMBI['success'])
		stockList=dataCMBI['result']['stockList']
		logging.info(f'{articleId} 包含的股票信息: {stockList}')
		# 名称，现价，涨跌幅
		stockNameList=jsonpath_getAll(stockList,'stockName')
		xjList=jsonpath_getAll(stockList,'xj')
		gainsList=jsonpath_getAll(stockList,'gains')
		self.assertNotIn(None,stockNameList)
		self.assertNotIn(None,xjList)
		self.assertNotIn(None,gainsList)

		logging.info(f' ========== 测试结束 资讯服务 ========== ')

	@no_retry
	@ddt.data('00700','哔哩哔哩','albb','!##$@')
	# @unittest.skip('跳过')
	def test_13_1_finInfoPageByValue(self,keyword):
		'''交易页股票搜索_新接口	'''
		logging.info(f' ========== 测试开始 交易页股票搜索_新接口 ========== ')

		url=f'{domainCMBI[self.args.env]}/gateway/order/stockNewSearch'
		dataJson={'inputSearch':keyword}
		logging.info(f'请求数据: {dataJson}')
		dataCMBI=postReq(0,dataJson,0,url=url,mod='post')
		logging.info(f'返回数据: {dataCMBI}')
		self.assertTrue(dataCMBI['success'])
		logging.info(f' ========== 测试结束 交易页股票搜索_新接口 ========== ')

	# @no_retry
	# @ddt.data('00700','哔哩哔哩','albb','!##$@')
	# # @unittest.skip('跳过')
	# def test_13_2_finInfoPageByValue(self,keyword):
	# 	'''交易页股票搜索_旧接口	'''
	# 	logging.info(f' ========== 测试开始 交易页股票搜索_旧接口	 ========== ')

	# 	url=f'{domainCMBI[self.args.env]}/gateway/order/stockSearch'
	# 	dataJson={'inputSearch':keyword}
		
	# 	session=getToken(self.args.account,self.pword,self.args.env,self.args.getTokenFromRedis)
	# 	dataJson.update(session)
	# 	logging.info(f'请求数据: {dataJson}')
	# 	dataCMBI=postReq(0,dataJson,0,url=url,mod='post')
	# 	logging.info(f'返回数据: {dataCMBI}')
	# 	self.assertTrue(dataCMBI['success'])
	# 	logging.info(f' ========== 测试结束 交易页股票搜索_旧接口 ========== ')

	@no_retry
	@ddt.data('00700','哔哩哔哩','albb','!##$@')
	# @unittest.skip('跳过')
	def test_14_finInfoPageByValue(self,keyword):
		'''综合搜索'''
		logging.info(f' ========== 测试开始 综合搜索 ========== ')

		url=f'{domainCMBI[self.args.env]}/search-center/public/es/v2/searchFinInfoPageByValue'
		dataJson={
			'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",
			'finFrom':'0',
			'finSize':'3',
			'infoFrom':'0',
			'infoSize':'3',
			'searchValue':keyword,
		}
		logging.info(f'请求数据: {dataJson}')
		dataCMBI=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {dataCMBI}')
		self.assertTrue(dataCMBI['success'])
		# 返回样式不变
		logging.info(f' ========== 测试结束 综合搜索 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	def test_15_getHostSearchList(self):
		'''热门搜索无退市股票'''
		logging.info(f' ========== 测试开始 热门搜索无退市股票 ========== ')

		url=f'{domainCMBI[self.args.env]}/gateway/fund/getHostSearchList'
		dataJson={'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='post')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		from client import getQotToken
		getQotToken(self.args.account,self.pword,self.args.env,self.args)
		path='/quote-query/qot/snapshot'
		for item in respJson['result']:
			if item['type']=='stock':
				
				dataJson={
					"marketCode":item['productId'][0],
					"stockCode":item['productId'][1:]
				}
				logging.info(f'请求聚源数据: {dataJson}')
				dataJY=postReq(path,dataJson,self.args.env,qotToken=self.args.qotToken)
				logging.info(f'聚源返回数据: {dataJY}')
				secStatus=jsonpath_getOne(dataJY,'secStatus')# suspend 是否停牌;secStatus=12表示退市
				self.assertNotEqual(secStatus,12)
		logging.info(f' ========== 测试结束 热门搜索无退市股票 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## node 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()