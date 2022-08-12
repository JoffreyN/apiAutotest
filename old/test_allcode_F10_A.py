import time
from common.database import queryCodelist
from common.tools import postReq,saveTodatabase,formatSqlStr

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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allcode_F10_HK.Log'))

################################################################################################################
# A股F10 相关接口美股码表遍历测试
from config import domainCMBI,assertObj,dataBaseInfo

env='dev'
# sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' AND sec_type=3;"
sql="SELECT market_code,stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND sec_type=3 AND (market_code='B' OR market_code='A');"
allCode=queryCodelist(0,0,sql,'test')
# market_code= E B A N
logging.info(f'股票代码共 {len(allCode)} 个')

pathList=[
	'/doraemon/hsf10/announcements',
	'/doraemon/hsf10/brief',
	'/doraemon/hsf10/finance',
	'/doraemon/hsf10/newsList',
	'/doraemon/hsf10/reportList',
]
#########################################http###################################################################
def test_F10_HK(stockCode,path):
	stockCode=''.join(stockCode)
	
	dataJson={'marketAndCode':stockCode}
	_start=time.perf_counter()
	respJson=postReq(0,dataJson,0,url=f'{domainCMBI[env]}{path}',mod='get',nolog=1)
	elapsed=round((time.perf_counter()-_start)*1000,2)
	
	try:
		assertObj.assertTrue(respJson['success'])
		logging.info(f'{path} {stockCode} 测试通过 接口耗时: {elapsed} ms')
		success,reason=1,0
	except (AssertionError,KeyError):
		success=0
		try:reason=respJson['errorMsg']
		except KeyError:reason='返回数据异常'
		if reason==None:
			logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}')
		else:
			logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=True)
	
	created_at=time.strftime('%Y-%m-%d %X')
	sql=f"INSERT INTO interfaceTest_data.f10_A_2 (created_at,path,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
	saveTodatabase(sql)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def startTest(path):
		for code in allCode:
			try:
				test_F10_HK(code,path)
			except:
				logging.error(f'{code} {path} 发生异常:',exc_info=True)
	
	###################################################################
	import threading
	threads=[]
	for path in pathList:
		t=threading.Thread(target=startTest,args=(path,))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')