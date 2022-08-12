import time
from common.database import queryCodelist,getDBconn,excuteSQL
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allcode_F10_HK_sellShort.Log'))

################################################################################################################
# 港股F10 相关接口美股码表遍历测试
from config import domainCMBI,assertObj

env='prod'
sql="SELECT stock_code FROM test_quote_sync.t_stock_info_prod WHERE enable_search=1 AND market_code='E' AND sec_type=3;"
# sql="SELECT stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;"
allCode=queryCodelist(0,0,sql,'test')
# market_code= E B A N
logging.info(f'股票代码共 {len(allCode)} 个')


#########################################http###################################################################
def test_F10_HK_sellShort(stockCode):
	stockCode=f'E{stockCode}'
	path='/doraemon/hkf10/sellShort'
	dataJson={'marketAndCode':stockCode}
	_start=time.perf_counter()
	respJson=postReq(0,dataJson,0,url=f'{domainCMBI[env]}{path}',mod='get',nolog=1)
	elapsed=round((time.perf_counter()-_start)*1000,2)
	try:
		assertObj.assertTrue(respJson['success'])
		try:
			tradingDay_0=respJson['result'][0]['tradingDay']
		except:
			tradingDay_0='无数据'
		if tradingDay_0 in ['2021-03-26','2021-03-29']:
			logging.info(f'{path} {stockCode} 测试通过 接口耗时: {elapsed} ms')
			success,reason=1,0
		else:
			logging.info(f'{path} {stockCode} 测试失败 接口耗时: {elapsed} ms')
			success,reason=0,tradingDay_0
	except (AssertionError,KeyError):
		success=0
		try:reason=respJson['errorMsg']
		except KeyError:reason='返回数据异常'
		if reason==None:
			logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}')
		else:
			logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=True)
	
	created_at=time.strftime('%Y-%m-%d %X')
	sql=f"INSERT INTO interfaceTest_data.f10_HK_sellshort (created_at,path,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
	saveTodatabase(sql)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def start_fuc(a,b):
		for code in allCode[a:b]:
			try:
				test_F10_HK_sellShort(code[0])
			except:
				logging.error(f'{code} 发生异常:',exc_info=True)

	def getSplit(data_len,ths):
		t=int(data_len/ths)
		splits=[i*t for i in range(ths+1)]
		splits[-1]=data_len
		return splits
	###################################################################
	import threading
	threads=[];thread_num=50
	splits=getSplit(len(allCode),thread_num)
	for i in range(thread_num):
		t=threading.Thread(target=start_fuc,args=(splits[i],splits[i+1]))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')
