import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq
from config import domainCMBI
from testData.data import codeDataUS_F10_list

# 1 /doraemon/financialDataUs/brief/findBriefData  美股F10-获取简介Tab信息
# 2 /doraemon/financialDataUs/brief/findCompanyExecutives  美股F10-获取简介-公司高管更多信息
# 3 /doraemon/financialDataUs/brief/findEquityShareholders  美股F10-获取简介-股本股东更多信息
# 4 /doraemon/financialDataUs/brief/findShareholdingChange  美股F10-获取简介-持股变动更多信息
# 5 /doraemon/financialDataUs/financial/findFinance  美股F10-获取财务Tab信息
# 6 /financialDataUs/financial/findFinanceList		美股F10-获取财务-财务报表
# 7 /financialDataUs/financial/findFinanceSheet		美股F10-获取三大表
# 8 /doraemon/financialDataUs/financial/findMainIndices  美股F10-获取财务-主营业务更多信息

# @unittest.skip('跳过')
@ddt.ddt
class TestF10_US(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 美股F10 接口测试开始 ########## ')

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_01_findBriefData(self,codeData):
		'''获取简介Tab信息'''
		logging.info(f' ========== 测试开始 获取简介Tab信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/brief/findBriefData'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取简介Tab信息 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_02_findCompanyExecutives(self,codeData):
		'''获取简介-公司高管更多信息'''
		logging.info(f' ========== 测试开始 获取简介-公司高管更多信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/brief/findCompanyExecutives'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取简介-公司高管更多信息 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_03_findEquityShareholders(self,codeData):
		'''获取简介-股本股东更多信息'''
		logging.info(f' ========== 测试开始 获取简介-股本股东更多信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/brief/findEquityShareholders'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取简介-股本股东更多信息 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_04_findShareholdingChange(self,codeData):
		'''获取简介-持股变动更多信息'''
		logging.info(f' ========== 测试开始 获取简介-持股变动更多信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/brief/findShareholdingChange'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取简介-持股变动更多信息 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_05_findFinance(self,codeData):
		'''获取财务Tab信息'''
		logging.info(f' ========== 测试开始 获取财务Tab信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findFinance'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取财务Tab信息 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_06_findFinanceList(self,codeData):
		'''获取财务-财务报表'''
		logging.info(f' ========== 测试开始 获取财务-财务报表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findFinanceList'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取财务-财务报表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_07_01_findFinanceSheet(self,codeData):
		'''获取三大表-利润表'''
		logging.info(f' ========== 测试开始 获取三大表-利润表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findFinanceSheet'
		dataJson={
			'indexType':'01',
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取三大表-利润表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_07_02_findFinanceSheet(self,codeData):
		'''获取三大表-资产负债表'''
		logging.info(f' ========== 测试开始 获取三大表-资产负债表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findFinanceSheet'
		dataJson={
			'indexType':'02',
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取三大表-资产负债表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_07_03_findFinanceSheet(self,codeData):
		'''获取三大表-现金流量表'''
		logging.info(f' ========== 测试开始 获取三大表-现金流量表 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findFinanceSheet'
		dataJson={
			'indexType':'03',
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取三大表-现金流量表 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*codeDataUS_F10_list)
	def test_08_findMainIndices(self,codeData):
		'''获取财务-主营业务更多信息'''
		logging.info(f' ========== 测试开始 获取财务-主营业务更多信息 ========== ')

		url=f'{domainCMBI[self.args.env]}/doraemon/financialDataUs/financial/findMainIndices'
		dataJson={
			'endDate':time.strftime('%Y%m%d'),
			'stockCode':codeData[1],
			'traceLogId':f"FromZP{time.time()}",
		}
		logging.info(f'请求数据: {dataJson}')
		respJson=postReq(0,dataJson,0,url=url,mod='get')
		logging.info(f'返回数据: {respJson}')
		self.assertTrue(respJson['success'])
		logging.info(f' ========== 测试结束 获取财务-主营业务更多信息 ========== ')


	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 美股F10 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()