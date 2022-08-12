import time,logging,traceback,unittest,numpy
from HTMLReport import ddt,no_retry

from common.parameter import ParameTestCase
from common.tools import postReq,getStockdata,genCodeData,jsonpath_getOne,getDayMoneyFlow,getToken,isTradeTime
from config import marketCodeDic,accountPool
from client import getQotToken
from testData.data import codeData,codeData_activelist,dataForZixuan,codeDataUS_F10_list
# @unittest.skip('跳过')
@ddt.ddt
class TestQuotation(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## quote-query接口测试开始 ########## ')

	def setUp(self):
		self.flag=True
		pword=accountPool[self.args.env][self.args.account]
		getQotToken(self.args.account,pword,self.args.env,self.args)

	def assertCom_GF(self,codeData,dataJY,dataGF,detail=0):
		# timeJY=dataJY['result']['basic']['updateTime'].replace(' ','').replace(':','').replace('-','')[:12]
		# timeGF=str(dataGF['quote']['data']['time'])[:12]# 仅精确到分
		# self.assertEqual(timeJY,timeGF)
		self.assertEqual(jsonpath_getOne(dataJY,'name','str'),jsonpath_getOne(dataGF,'name','str'))
		self.assertEqual(jsonpath_getOne(dataJY,'code','str'),jsonpath_getOne(dataGF,'code','str'))
		ampRate=100
		if codeData[3] in [101,105]:# A股
			rate=100
		else:# 港股
			rate=1000
		self.assertNumber('最高',jsonpath_getOne(dataJY,'highPrice'),jsonpath_getOne(dataGF,'high')/rate)
		self.assertNumber('最低',jsonpath_getOne(dataJY,'lowPrice'),jsonpath_getOne(dataGF,'low')/rate)
		self.assertNumber('今开',jsonpath_getOne(dataJY,'openPrice'),jsonpath_getOne(dataGF,'open')/rate)
		self.assertNumber('昨收',jsonpath_getOne(dataJY,'lastClosePrice'),jsonpath_getOne(dataGF,'pclose')/rate)
		self.assertNumber('成交额',jsonpath_getOne(dataJY,'turnover'),jsonpath_getOne(dataGF,'amount')/rate)
		if detail:
			if codeData[0]=='zhishu':# 指数
				self.assertNumber('上涨支数',jsonpath_getOne(dataJY,'raiseCount'),jsonpath_getOne(dataGF,'rise'))
				self.assertNumber('下跌支数',jsonpath_getOne(dataJY,'fallCount'),jsonpath_getOne(dataGF,'fall'))
				self.assertNumber('平盘支数',jsonpath_getOne(dataJY,'equalCount'),jsonpath_getOne(dataGF,'draw'))
				if A股指数:
					self.assertNumber('成交量',jsonpath_getOne(dataJY,'volume'),jsonpath_getOne(dataGF,'volume'))
			else:# 个股
				self.assertNumber('成交量',jsonpath_getOne(dataJY,'volume'),jsonpath_getOne(dataGF,'volume'))
				self.assertNumber('振幅',jsonpath_getOne(dataJY,'amplitude'),jsonpath_getOne(dataGF,'amp')/ampRate)
				if dataJY['result']['warrant']:
					self.assertNumber('每手股数',jsonpath_getOne(dataJY,'lotSize'),jsonpath_getOne(dataGF,'trading_unit'))
					self.assertNumber('行权价格',jsonpath_getOne(dataJY,'strikePrice'),jsonpath_getOne(dataGF,'strike')/rate)
				else:
					self.assertNumber('平均价',jsonpath_getOne(dataJY,'avgPrice'),jsonpath_getOne(dataGF,'avg')/rate)
					self.assertNumber('总股本',jsonpath_getOne(dataJY,'issuedShares'),jsonpath_getOne(dataGF,'total'))
					if codeData[3]==161:# 港股
						self.assertNumber('流通市值',jsonpath_getOne(dataJY,'outstandingMarketVal'),jsonpath_getOne(dataGF,'circulation_value')/rate)
						self.assertNumber('市盈率（静态）',jsonpath_getOne(dataJY,'staticPeRate'),jsonpath_getOne(dataGF,'pe')/rate)
						self.assertNumber('委比',jsonpath_getOne(dataJY,'bidAskRatio'),jsonpath_getOne(dataGF,'cittthan')/rate)
						self.assertNumber('量比',jsonpath_getOne(dataJY,'volumeRatio'),jsonpath_getOne(dataGF,'volume_ratio')/rate)
						self.assertNumber('内盘',jsonpath_getOne(dataJY,'amountIn'),jsonpath_getOne(dataGF,'in')/rate)
						self.assertNumber('外盘',jsonpath_getOne(dataJY,'amountOut'),jsonpath_getOne(dataGF,'out')/rate)
						self.assertNumber('52周最低',jsonpath_getOne(dataJY,'highest52WeeksPrice'),jsonpath_getOne(dataGF,'high_p1y')/rate)
						self.assertNumber('52周最高',jsonpath_getOne(dataJY,'lowest52WeeksPrice'),jsonpath_getOne(dataGF,'low_p1y')/rate)
						self.assertNumber('换手率',jsonpath_getOne(dataJY,'turnoverRate'),jsonpath_getOne(dataGF,'turnover_rate')/rate)
						self.assertNumber('市净率',jsonpath_getOne(dataJY,'pbRate'),jsonpath_getOne(dataGF,'pb')/10000)
						self.assertNumber('每手股数',jsonpath_getOne(dataJY,'lotSize'),jsonpath_getOne(dataGF,trading_unit))
					elif codeData[3] in [101,105]:# A股
						self.assertNumber('市净率',jsonpath_getOne(dataJY,'pbRate'),jsonpath_getOne(dataGF,'pb')/rate)
						self.assertNumber('换手率',jsonpath_getOne(dataJY,'turnoverRate'),jsonpath_getOne(dataGF,'turnover_rate')/rate)
						self.assertNumber('涨停价',jsonpath_getOne(dataJY,'upPx'),jsonpath_getOne(dataGF,'price_upper_limit')/rate)
						self.assertNumber('跌停价',jsonpath_getOne(dataJY,'downPx'),jsonpath_getOne(dataGF,'price_low_limit')/rate)

	def assertCom_JL(self,codeData,dataJY,dataJL,detail=0):
		# timeJY=time.mktime(time.strptime(dataJY['result']['basic']['updateTime'],'%Y-%m-%d %X'))
		# timeJL=time.mktime(time.strptime(dataJL['data']['qt']['alltime'],'%Y-%m-%d %X'))
		# self.assertNumber('更新时间',timeJY,timeJL,300)
		volRate=100 if codeData[3] in [101,105] else 1
		code=jsonpath_getOne(dataJY,'code','str')
		if code=='000001':code='1A0001'
		# self.assertEqual(dataJY['result']['basic']['name'],dataJL['data']['name'])
		self.assertEqual(code,dataJL['data']['code'][1:])

		self.assertNumber(f'{code} 最高',jsonpath_getOne(dataJY,'highPrice'),jsonpath_getOne(dataJL,'hi'))
		self.assertNumber(f'{code} 最低',jsonpath_getOne(dataJY,'lowPrice'),jsonpath_getOne(dataJL,'lo'))
		self.assertNumber(f'{code} 今开',jsonpath_getOne(dataJY,'openPrice'),jsonpath_getOne(dataJL,'jk'))
		self.assertNumber(f'{code} 昨收',jsonpath_getOne(dataJY,'lastClosePrice'),jsonpath_getOne(dataJL,'zs'))
		self.assertNumber(f'{code} 成交量',jsonpath_getOne(dataJY,'volume'),jsonpath_getOne(dataJL,'zl')*volRate)
		self.assertNumber(f'{code} 成交额',jsonpath_getOne(dataJY,'turnover'),jsonpath_getOne(dataJL,'ze'))
		if detail:
			if codeData[0]=='zhishu':# 指数
				self.assertNumber(f'{code} 上涨支数',jsonpath_getOne(dataJY,'raiseCount'),jsonpath_getOne(dataJL,'csz'))
				self.assertNumber(f'{code} 下跌支数',jsonpath_getOne(dataJY,'fallCount'),jsonpath_getOne(dataJL,'cxd'))
				self.assertNumber(f'{code} 平盘支数',jsonpath_getOne(dataJY,'equalCount'),jsonpath_getOne(dataJL,'cpp'))
			else:
				self.assertNumber(f'{code} 振幅',jsonpath_getOne(dataJY,'amplitude'),jsonpath_getOne(dataJL,'zf'))
				self.assertNumber(f'{code} 每手股数',jsonpath_getOne(dataJY,'lotSize'),jsonpath_getOne(dataJL,'lot'))
				if not dataJY['result']['warrant']:#不是牛熊证、认购证
					# self.assertNumber(f'{code} 平均价',jsonpath_getOne(dataJY,'avgPrice'),jsonpath_getOne(dataJL,'jj'))# 捷力数据不准
					self.assertNumber(f'{code} 总市值',jsonpath_getOne(dataJY,'issuedMarketVal'),jsonpath_getOne(dataJL,'sz'))
					# self.assertNumber(f'{code} 委比',jsonpath_getOne(dataJY,'bidAskRatio'),jsonpath_getOne(dataJL,'wb'))# 捷力数据不准
					self.assertNumber(f'{code} 量比',jsonpath_getOne(dataJY,'volumeRatio'),jsonpath_getOne(dataJL,'lb'))
					# self.assertNumber(f'{code} 内盘',jsonpath_getOne(dataJY,'amountIn'),jsonpath_getOne(dataJL,'np')*volRate)
					# self.assertNumber(f'{code} 外盘',jsonpath_getOne(dataJY,'amountOut'),jsonpath_getOne(dataJL,'wp')*volRate)
					self.assertNumber(f'{code} 52周最低',jsonpath_getOne(dataJY,'lowest52WeeksPrice'),jsonpath_getOne(dataJL,'l52'))
					self.assertNumber(f'{code} 52周最高',jsonpath_getOne(dataJY,'highest52WeeksPrice'),jsonpath_getOne(dataJL,'h52'))
					self.assertNumber(f'{code} 换手率',jsonpath_getOne(dataJY,'turnoverRate'),jsonpath_getOne(dataJL,'hs'))
					# self.assertNumber(f'{code} 静市盈率',jsonpath_getOne(dataJY,'staticPeRate'),jsonpath_getOne(dataJL,'sy'))#捷力的数据都是错的
					self.assertNumber(f'{code} 流通股本',jsonpath_getOne(dataJY,'outstandingShares'),jsonpath_getOne(dataJL,'ltgb'))
					if codeData[3] in [101,105]:# A股
						self.assertNumber(f'{code} 涨停价',jsonpath_getOne(dataJY,'upPx'),round(jsonpath_getOne(dataJL,'zs')*1.1,2))
						self.assertNumber(f'{code} 跌停价',jsonpath_getOne(dataJY,'downPx'),round(jsonpath_getOne(dataJL,'zs')*0.9,2))

	def assertCom_FT(self,codeData,dataJY,dataFT,detail=0):
		code=jsonpath_getOne(dataJY,'code','str')
		# self.assertEqual(dataJY['result']['basic']['security']['code'],dataFT['code']['0'].split('.')[1])
		self.assertNumber(f'{code} 最高',jsonpath_getOne(dataJY,'highPrice'),dataFT['high_price']['0'])
		self.assertNumber(f'{code} 最低',jsonpath_getOne(dataJY,'lowPrice'),dataFT['low_price']['0'])
		self.assertNumber(f'{code} 今开',jsonpath_getOne(dataJY,'openPrice'),dataFT['open_price']['0'])
		self.assertNumber(f'{code} 昨收',jsonpath_getOne(dataJY,'lastClosePrice'),dataFT['prev_close_price']['0'])
		self.assertNumber(f'{code} 成交量',jsonpath_getOne(dataJY,'volume'),dataFT['volume']['0'])
		self.assertNumber(f'{code} 成交额',jsonpath_getOne(dataJY,'turnover'),dataFT['turnover']['0'])
		if detail:
			if codeData[0]=='zhishu':# 指数
				self.assertNumber(f'{code} 上涨支数',jsonpath_getOne(dataJY,'raiseCount'),dataFT['index_raise_count']['0'],1)
				self.assertNumber(f'{code} 下跌支数',jsonpath_getOne(dataJY,'fallCount'),dataFT['index_fall_count']['0'],1)
				self.assertNumber(f'{code} 平盘支数',jsonpath_getOne(dataJY,'equalCount'),dataFT['index_equal_count']['0'],1)
			else:
				self.assertNumber(f'{code} 振幅',jsonpath_getOne(dataJY,'amplitude'),dataFT['amplitude']['0'])
				self.assertNumber(f'{code} 每手股数',jsonpath_getOne(dataJY,'lotSize'),dataFT['lot_size']['0'],1)
				if dataJY['result']['warrant']:#是牛熊证、认购证
					pass
					# self.assertNumber(f'{code} 行权价格',jsonpath_getOne(dataJY,'strikePrice'),dataFT['option_strike_price']['0'])
				else:
					self.assertNumber(f'{code} 平均价',jsonpath_getOne(dataJY,'avgPrice'),dataFT['avg_price']['0'])
					self.assertNumber(f'{code} 总市值',jsonpath_getOne(dataJY,'issuedMarketVal'),dataFT['total_market_val']['0'])
					self.assertNumber(f'{code} 总股本',jsonpath_getOne(dataJY,'issuedShares'),dataFT['issued_shares']['0'])
					self.assertNumber(f'{code} 流通股本',jsonpath_getOne(dataJY,'outstandingShares'),dataFT['outstanding_shares']['0'])
					self.assertNumber(f'{code} 流通市值',jsonpath_getOne(dataJY,'outstandingMarketVal'),dataFT['circular_market_val']['0'])
					self.assertNumber(f'{code} 市盈率（静态）',jsonpath_getOne(dataJY,'staticPeRate'),dataFT['pe_ratio']['0'])
					self.assertNumber(f'{code} 市盈率（TTM）',jsonpath_getOne(dataJY,'ttmPeRate'),dataFT['pe_ttm_ratio']['0'])
					# self.assertNumber(f'{code} 市净率',jsonpath_getOne(dataJY,'pbRate'),dataFT['pb_ratio']['0'])
					self.assertNumber(f'{code} 委比',jsonpath_getOne(dataJY,'bidAskRatio'),dataFT['bid_ask_ratio']['0'])
					self.assertNumber(f'{code} 量比',jsonpath_getOne(dataJY,'volumeRatio'),dataFT['volume_ratio']['0'])
					self.assertNumber(f'{code} 52周最低',jsonpath_getOne(dataJY,'lowest52WeeksPrice'),dataFT['lowest52weeks_price']['0'])
					self.assertNumber(f'{code} 52周最高',jsonpath_getOne(dataJY,'highest52WeeksPrice'),dataFT['highest52weeks_price']['0'])
					# self.assertNumber(f'{code} 股息TTM ',jsonpath_getOne(dataJY,'dividendTTM'),dataFT['dividend_ttm']['0'])
					# self.assertNumber(f'{code} 股息率TTM ',jsonpath_getOne(dataJY,'dividendRatioTTM'),dataFT['dividend_ratio_ttm']['0'])
					# self.assertNumber(f'{code} 股息LFY ',jsonpath_getOne(dataJY,'dividendLFY'),dataFT['dividend_lfy']['0'])
					# self.assertNumber(f'{code} 股息率LFY ',jsonpath_getOne(dataJY,'dividendLFYRatio'),dataFT['dividend_lfy_ratio']['0'])
					# self.assertNumber(f'{code} 换手率',jsonpath_getOne(dataJY,'turnoverRate'),dataFT['turnover_rate']['0'])
					if codeData[3] in [101,105]:# A股
						self.assertNumber(f'{code} 涨停价',jsonpath_getOne(dataJY,'upPx'),round(dataFT['prev_close_price']['0']*1.1,2))
						self.assertNumber(f'{code} 跌停价',jsonpath_getOne(dataJY,'downPx'),round(dataFT['prev_close_price']['0']*0.9,2))

	def assertNumber(self,msg,num1,num2,r=0,kexue=0):
		if numpy.isnan(num2):num2=0
		if kexue:
			if num1>1000000:# 大于一百万则转换为科学计数法，分别对比数字及指数
				num1,e1=map(float,("%.5e"%num1).split('e+'))
				num2,e2=map(float,("%.5e"%num2).split('e+'))
				self.assertEqual(e1,e2)
		c=abs(round(num1-num2,3))
		if r:
			d=999999999 if c!=0 else 0
		else:
			try:
				d=abs(num1-num2)/abs(num1)
			except ZeroDivisionError:
				d=abs(num1-num2)/0.00000000001
		if d>=0.5:
			self.flag=False
			__='<<<--------------------'
		else:
			__=''
		resultTxt=f'{msg} 差值: |{num1}-{num2}|={c}  {d}'
		resultTxt2=f'{msg} 差值: |{num1}-{num2}|={c}  {d}  {__}'
		if d>0:
			with open(f'result_{self.args.timeStr}.txt','a',encoding='utf-8') as file:
				file.write(f'{resultTxt}\n')
		logging.info(resultTxt2)
		# if c>=r:self.flag=False

	###############################################################################################################################################
	# @no_retry
	# @unittest.skip('跳过')
	# @ddt.data(*genCodeData(lens=20,env='test'))
	# @ddt.data(*codeDataUS_F10_list)
	# @ddt.data(*[('US','BSCM','BSCM',303),('US','VHC','VHC',303),])
	@ddt.data(*codeData_activelist)
	def test_1_snapshot(self,codeData):
		'''行情快照'''
		logging.info(f' ========== 测试开始 {codeData[1]}_{codeData[2]} 行情快照 ========== ')
		if codeData[3]==303 and codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 没有美股指数权限')
		path='/quote-query/qot/snapshot'
		dataJson={
			"marketCode":marketCodeDic[codeData[3]],
			"stockCode":codeData[1]
		}
		logging.info(f'请求聚源数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env,qotToken=self.args.qotToken)
		logging.info(f'聚源返回数据: {dataJY}')
		if self.args.compare=='gf':
			dataGF=getStockdata(codeData[1],codeData[3])
			logging.info(f'广发返回数据: {dataGF}')
			self.assertCom_GF(codeData,dataJY,dataGF,1)
		elif self.args.compare=='jl':
			if codeData[1]=='000001':codeData[1]='1A0001'
			dataJL=getStockdata(codeData[1],marketCodeDic[codeData[3]],source='jl')
			dataJL['data']['que']=''
			dataJL['data']['tk']=''
			dataJL['data']['ol']=''
			logging.info(f'捷力返回数据: {dataJL}')
			self.assertCom_JL(codeData,dataJY,dataJL,1)
			self.assertTrue(self.flag)
		elif self.args.compare=='ft':
			dataFT=getStockdata(codeData[1],codeData[3],source='ft')
			logging.info(f'富途返回数据: {dataFT}')
			self.assertCom_FT(codeData,dataJY,dataFT,1)
			self.assertTrue(self.flag)
		else:
			self.assertIsNotNone(jsonpath_getOne(dataJY,'lastClosePrice'))
		logging.info(f' ========== 测试结束 {codeData[1]}_{codeData[2]} 行情快照 ========== ')
	
	# @no_retry
	# # @unittest.skip('跳过')
	# # @ddt.data(*genCodeData(lens=20,env='test'))
	# # @ddt.data(*codeDataUS_F10_list)
	# @ddt.data(*codeData_activelist)
	# def test_2_timeShare(self,codeData):
	# 	'''分时数据'''
	# 	logging.info(f' ========== 测试开始 {codeData[1]}_{codeData[2]} 分时数据 ========== ')
	# 	if codeData[3]==303 and codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 没有美股指数权限')
	# 	path='/quote-query/quote/timeShare'
	# 	dataJson={
	# 		"marketCode":marketCodeDic[codeData[3]],
	# 		"stockCode":codeData[1]
	# 	}
	# 	logging.info(f'请求聚源数据: {dataJson}')
	# 	dataJY=postReq(path,dataJson,self.args.env)
	# 	try:minutes=len(dataJY['result'])
	# 	except TypeError:minutes=0
	# 	if minutes<=0:logging.info(f'聚源返回数据: {dataJY}')
	# 	# logging.info(f'聚源返回数据: {dataJY}')
	# 	logging.info(f'分时个数: {minutes}')
	# 	self.assertGreater(minutes,0)
	# 	logging.info(f' ========== 测试结束 {codeData[1]}_{codeData[2]} 分时数据 ========== ')
	
	@no_retry
	# @ddt.data(*genCodeData(lens=20,env='test'))
	# @unittest.skip('跳过')
	@ddt.data((10000,1,1,0),(200,1,1,1),(10,1,2,0),(0,1,3,1),(100,0,4,0),(100,1,5,1),(100,0,6,0),(100,1,7,1),(100,0,8,0),(100,1,9,1))
	@ddt.unpack
	def test_3_kline(self,conut,direction,kline,rehab):
		'''K线数据'''
		logging.info(f' ========== 测试开始 K线数据 ========== ')
		path='/quote-query/qot/kline'
		dataJson={
			"count":conut,
			"date":time.strftime('%Y%m%d'),
			"direction":direction,
			"kline":kline,
			"marketCode":"E",
			"min":0,
			"rehab":rehab,
			"stockCode":"00700"
		}
		logging.info(f'请求聚源数据: {dataJson}')
		dataJY=postReq(path,dataJson,self.args.env,qotToken=self.args.qotToken)
		# logging.info(f'聚源返回数据: {dataJY}')
		num=len(dataJY['result'])
		logging.info(f'K线个数: {num}')
		if num<=0:logging.info(f'聚源返回数据: {dataJY}')
		self.assertGreater(num,0)
		logging.info(f' ========== 测试结束 K线数据 ========== ')

	@no_retry
	# @unittest.skip('跳过')
	@ddt.data(*dataForZixuan)
	def test_4_personalStocks(self,codeDic):
		'''自选股列表行情'''
		logging.info(f' ========== 测试开始 自选股列表行情 ========== ')
		# path='/quote-query/quote/personalStocks'
		path='/quote-query/qot/watchlist'
		dataJson={'codes':codeDic['codeList']}
		# codeDic['codeList']=['E00700','A300760','B600519']
		# codeDic['codeList']=['E00700','A300760','B600519','NBILI']
		logging.info(f"请求聚源数据: {dataJson}")
		dataJY=postReq(path,dataJson,self.args.env,qotToken=self.args.qotToken)
		logging.info(f'聚源返回数据: {dataJY}')
		
		self.assertEqual(len(dataJY['result']),len(codeDic['codeList']))
		logging.info(f' ========== 测试结束 自选股列表行情 ========== ')

	# @no_retry
	# # @unittest.skip('跳过')
	# # @ddt.data(*genCodeData(lens=20,env='test'))
	# # @ddt.data(*codeDataUS_F10_list)
	# @ddt.data(*codeData_activelist)
	# def test_5_fiveLevel(self,codeData):
	# 	'''五档行情'''
	# 	logging.info(f' ========== 测试开始 五档行情 ========== ')
	# 	if codeData[0]=='zhishu':self.skipTest(f'{codeData[1]} 指数没有买卖档')
	# 	path='/quote-query/quote/fiveLevelQuotation'
	# 	pword=accountPool[self.args.env][self.args.account]
	# 	loginToken=getToken(self.args.account,pword,self.args.env,self.args.getTokenFromRedis)['token']

	# 	dataJson={
	# 		"clickAt":int(time.time()),
	# 		"deviceId":"zp_InterfaceTest",
	# 		"deviceType":"python3",
	# 		"loginAt":int(time.time()),
	# 		"realTime":False,
	# 		"sourceIp":"深圳南山区",
	# 		"marketCode":marketCodeDic[codeData[3]],
	# 		"stockCode":codeData[1],
	# 		"token":loginToken,
	# 		"userId":self.args.account
	# 	}
	# 	logging.info(f'请求聚源数据: {dataJson}')
	# 	dataJY=postReq(path,dataJson,self.args.env)
	# 	logging.info(f'聚源返回数据: {dataJY}')
	# 	self.assertIsNotNone(dataJY['result'])
	# 	# self.assertTrue(dataJY['success'])
	# 	# buy1=dataJY['result']['buy'][0]['price']
	# 	# sell1=dataJY['result']['sell'][0]['price']
	# 	# buyVol=dataJY['result']['buy'][0]['volume']
	# 	# sellVol=dataJY['result']['sell'][0]['volume']
	# 	# self.assertGreaterEqual(sell1,buy1)
	# 	# self.assertGreaterEqual(buyVol*sellVol,0)
	# 	logging.info(f' ========== 测试结束 五档行情 ========== ')

	# @no_retry
	# # @unittest.skip('跳过')
	# def test_6_forOtherService(self):
	# 	'''给其他服务提供行情快照源服务'''
	# 	logging.info(f' ========== 测试开始 给其他服务提供行情快照源服务 ========== ')
	# 	path='/quote-query/quote/forOtherService'
	# 	dataJson={'codes':["E00700","A300760","B600519"]}
	# 	logging.info(f'请求聚源数据: {dataJson}')
	# 	dataJY=postReq(path,dataJson,self.args.env)
	# 	logging.info(f'聚源返回数据: {dataJY}')
	# 	self.assertTrue(dataJY['success'])
	# 	logging.info(f' ========== 测试结束 给其他服务提供行情快照源服务 ========== ')

	# @no_retry
	# # @unittest.skip('跳过')
	# @ddt.data(*[("E","HK2SH"),("E","HK2SZ"),("B","SH2HK"),("A","SZ2HK")])
	# def test_7_compareMoneyFlow(self,data):
	# 	'''南下北上资金流对比'''
	# 	if time.strftime('%w') in '06':self.skipTest("跳过周末")
	# 	date=time.strftime('%Y%m%d')
	# 	startTime1=time.mktime(time.strptime(f'{date} 16:10:00','%Y%m%d %X'))
	# 	startTime2=time.mktime(time.strptime(f'{date} 23:40:00','%Y%m%d %X'))
	# 	if startTime1<time.time()<startTime2:
	# 		info={"HK2SH":"南下港股通(沪)","HK2SZ":"南下港股通(深)","SH2HK":"北上沪股通","SZ2HK":"北上深股通",}
	# 		logging.info(f' ========== 测试开始 {info[data[1]]} 资金流入对比 ========== ')
	# 		url='http://rhino-proxy-test.cmbi.online/api/quotation/sync/timeshare'
	# 		dataJson={'marketCode':data[0],'stockCode':data[1]}
	# 		logging.info(f'请求聚源数据: {dataJson}')
	# 		dataJY=postReq(path=0,dataJson=dataJson,url=url,env=self.args.env)
	# 		logging.info(f'聚源返回数据: {dataJY[-1]}')
	# 		flowIn_JY=f"{round(float(dataJY[-1]['flowIn'])/100000000,2)}亿元"
	# 		logging.info( f"{info[data[1]]} 当日资金流入: {flowIn_JY}")
	# 		self.assertGreater(len(dataJY),0)

	# 		flowIn_XL=getDayMoneyFlow()
	# 		logging.info(f'新浪数据: {flowIn_XL}')
	# 		self.assertEqual(flowIn_XL[data[1]],flowIn_JY)
	# 		logging.info(f' ========== 测试开始 {info[data[1]]} 资金流入对比 ========== ')
	# 	else:
	# 		self.skipTest("跳过，不是收盘时间")
	
	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## quote-query接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()