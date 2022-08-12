import time
from common.database import queryCodelist
from common.tools import postReq,jsonpath_getOne,jsonpath_getAll,saveTodatabase,formatSqlStr
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allCode_snapshot_timeShare.Log'))

################################################################################################################
# 此遍历脚本验证问题：
# 1、美股周K昨收价格为0

env='test'
sql="SELECT market_code,stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='N' AND delisting=0;"
allCode=queryCodelist(0,0,sql,env)

from config import domainJY,assertObj

#########################################http###################################################################
def kline(mk,code):
	path='/quote-query/quote/kline'
	dataJson={
		"count":3,"direction":1,"kline":3,"rehab":0,
		"marketCode":mk,"stockCode":code
	}
	respJson=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	lastClosePrices=jsonpath_getAll(respJson,'lastClosePrice')

	try:
		assertObj.assertTrue(all(map(lambda x:x>0,lastClosePrices)))
		failed_reason=''
		logging.info(f'{mk}{code} 周K昨收价格大于0测试通过')
	except AssertionError:
		failed_reason='周K昨收价格有不大于0的值;'
		logging.info(f'{mk}{code} 周K昨收价格有不大于0的值: {respJson}')
	except:
		failed_reason=f'周K昨收价格 断言发生其它异常，详见日志;'
		logging.info(f'{mk}{code} 返回数据: {respJson}\n发生其它异常:',exc_info=True)


	success=0 if failed_reason else 1
	created_at=time.strftime('%Y-%m-%d %X')
	saveSQL=f"INSERT INTO interfaceTest_data.weekKline_1 (created_at,stockCode,req_data,success,failed_reason,respJson) VALUES ('{created_at}','{code}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson)}');"
	saveTodatabase(saveSQL)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def startTest(a,b):
		for item in allCode[a:b]:
			try:
				kline(*item)
			except:
				logging.error(f'{item} 发生异常:',exc_info=True)

	def getSplit(data_len,ths):
		t=int(data_len/ths)
		splits=[i*t for i in range(ths+1)]
		splits[-1]=data_len
		return splits
	###################################################################
	import threading
	threads=[];thread_num=10
	splits=getSplit(len(allCode),thread_num)
	for i in range(thread_num):
		t=threading.Thread(target=startTest,args=(splits[i],splits[i+1]))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')