import time
from common.database import queryCodelist
from common.tools import postReq
################################################################################################################
import logging
from HTMLReport.src.tools.log.handler_factory import HandlerFactory
for handler in logging.getLogger().handlers:
	if not handler.get_name():
		logging.getLogger().removeHandler(handler)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(HandlerFactory.get_std_out_handler())
logging.getLogger().addHandler(HandlerFactory.get_std_err_handler())
logging.getLogger().addHandler(HandlerFactory.get_stream_handler())
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('testAllcode.Log'))

################################################################################################################
# 聚源行情相关接口码表遍历测试

env='test'
sql="SELECT market_code,stock_code FROM t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A');"
allCode=queryCodelist(0,0,sql,env)
# allCode=queryCodelist(0,0,"SELECT market_code,stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;")
# market_code= E B A N
from config import domainJY,assertObj

#########################################http###################################################################
def snapshot(mk,code):
	path='/quote-query/quote/snapshot'
	dataJson={"marketCode":mk,"stockCode":code}
	dataJY=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	try:
		assertObj.assertTrue(dataJY['success'])
		assertObj.assertIsNotNone(dataJY['result'])
		logging.info(f'snapshot {mk}{code} 测试通过')
	except AssertionError:
		logging.info(f'snapshot {mk}{code} 请求数据: {dataJson}\n返回数据: {dataJY}\n断言失败:',exc_info=True)

def timeShare(mk,code):
	path='/quote-query/quote/timeShare'
	dataJson={"marketCode":mk,"stockCode":code}
	dataJY=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	try:
		assertObj.assertTrue(dataJY['success'])
		assertObj.assertGreater(len(dataJY['result']),0)
		logging.info(f'timeShare {mk}{code} 测试通过')
	except AssertionError:
		logging.info(f'timeShare {mk}{code} 请求数据: {dataJson}\n返回数据: {dataJY}\n断言失败:',exc_info=True)

def kline(mk,code):
	path='/quote-query/quote/kline'
	dataJson={
		"count":200,"date":time.strftime('%Y%m%d'),"direction":1,
		"kline":1,"marketCode":mk,"min":0,"rehab":0,"stockCode":code
	}
	# logging.info(f'kline 请求数据: {dataJson}')
	dataJY=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	try:
		assertObj.assertTrue(dataJY['success'])
		assertObj.assertGreater(len(dataJY['result']),0)
		logging.info(f'kline {mk}{code} 测试通过')
	except AssertionError:
		logging.info(f'kline {mk}{code} 请求数据: {dataJson}\n返回数据: {dataJY}\n断言失败:',exc_info=True)

def fiveLevel(mk,code):
	path='/quote-query/quote/fiveLevelQuotation'
	dataJson={"marketCode":mk,"stockCode":code}
	dataJY=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	try:
		assertObj.assertTrue(dataJY['success'])
		assertObj.assertLessEqual(dataJY['result']['buy'][0]['price'],dataJY['result']['sell'][0]['price'])
		assertObj.assertGreaterEqual(dataJY['result']['buy'][0]['volume']*dataJY['result']['sell'][0]['volume'],0)
		logging.info(f'fiveLevel {mk}{code} 测试通过')
	except AssertionError:
		logging.info(f'fiveLevel {mk}{code} 请求数据: {dataJson}\n返回数据: {dataJY}\n断言失败:',exc_info=True)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info('测试开始')
	###################################################################
	def start_fiveLevel():
		for mkCode in allCode:
			try:
				fiveLevel(mkCode[0],mkCode[1])
			except:
				logging.error(f'{mkCode} 发生异常:',exc_info=True)

	def start_kline():
		for mkCode in allCode:
			try:
				kline(mkCode[0],mkCode[1])
			except:
				logging.error(f'{mkCode} 发生异常:',exc_info=True)

	def start_snapshot():
		for mkCode in allCode:
			try:
				snapshot(mkCode[0],mkCode[1])
			except:
				logging.error(f'{mkCode} 发生异常:',exc_info=True)


	def start_timeShare():
		for mkCode in allCode:
			try:
				timeShare(mkCode[0],mkCode[1])
			except:
				logging.error(f'{mkCode} 发生异常:',exc_info=True)
	###################################################################
	import threading
	threads=[]
	for func in [start_fiveLevel,start_kline,start_snapshot,start_timeShare,]:
		t=threading.Thread(target=func)
		threads.append(t)
		t.start()
	for t in threads:
		t.join()

	# thread_fiveLevel=threading.Thread(target=start_fiveLevel)
	# thread_kline=threading.Thread(target=start_kline)

	# thread_fiveLevel.start()
	# thread_kline.start()

	# thread_fiveLevel.join()
	# thread_kline.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')