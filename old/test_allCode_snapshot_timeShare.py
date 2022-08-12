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
# 此遍历脚本验证以下两个问题：
# 1、分时价格为负数
# 2、分时和快照昨收价格不相等

env='test'
sql="SELECT market_code,stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='N' AND status!='INVALID'"
allCode=queryCodelist(0,0,sql,env)
# allCode=eval(open('testData/selfStock.txt','r',encoding='utf-8').read())

# allCode=queryCodelist(0,0,"SELECT market_code,stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;")
# market_code= E B A N
from config import domainJY,assertObj

#########################################http###################################################################
def snapshot_timeShare(mk,code):
	path_snapshot='/quote-query/quote/snapshot'
	dataJson={"marketCode":mk,"stockCode":code}
	resp_snapshot=postReq(0,dataJson,env,url=f'{domainJY[env]}{path_snapshot}',nolog=1)
	lastClosePrice_snapshot=round(jsonpath_getOne(resp_snapshot,'lastClosePrice','float'),2)

	path_timeShare='/quote-query/quote/timeShare'
	resp_timeshare=postReq(0,dataJson,env,url=f'{domainJY[env]}{path_timeShare}',nolog=1)
	lastClosePrice_timeshare=round(jsonpath_getOne(resp_timeshare,'lastClosePrice','float'),2)
	price_timeshares=jsonpath_getAll(resp_timeshare,'price')

	try:
		assertObj.assertEqual(lastClosePrice_snapshot,lastClosePrice_timeshare)
		failed_reason=''
		logging.info(f'{mk}{code} 昨收对比测试通过')
	except AssertionError:
		failed_reason=f'昨收断言失败 {lastClosePrice_snapshot}!={lastClosePrice_timeshare};'
		logging.info(f'{mk}{code} snapshot返回数据: {resp_snapshot}\ntimeShare返回数据: {resp_timeshare}\n昨收断言失败:',exc_info=True)
	except:
		failed_reason=f'昨收断言发生其它异常，详见日志;'
		logging.info(f'{mk}{code} snapshot返回数据: {resp_snapshot}\ntimeShare返回数据: {resp_timeshare}\n发生其它异常:',exc_info=True)

	try:
		assertObj.assertTrue(all(map(lambda x:x>=0,price_timeshares)))
		failed_reason=failed_reason
		logging.info(f'{mk}{code} 分时价格大于0测试通过')
	except AssertionError:
		failed_reason=f'{failed_reason}分时价格有负数;'
		logging.info(f'{mk}{code} timeShare返回 分时价格有负数: {resp_timeshare}')
	except:
		failed_reason=f'{failed_reason}分时价格断言发生其它异常，详见日志;'
		logging.info(f'{mk}{code} timeShare返回数据: {resp_timeshare}\n发生其它异常:',exc_info=True)

	success=0 if failed_reason else 1
	created_at=time.strftime('%Y-%m-%d %X')
	saveSQL=f"INSERT INTO interfaceTest_data.snapshot_timeShare_2 (created_at,stockCode,req_data,success,failed_reason,resp_snapshot,resp_timeshare) VALUES ('{created_at}','{code}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(resp_snapshot)}','{formatSqlStr(resp_timeshare)}');"
	saveTodatabase(saveSQL)

def count_snapshot_curPrice(mk,code):
	path_snapshot='/quote-query/quote/snapshot'
	dataJson={"marketCode":mk,"stockCode":code}
	resp_snapshot=postReq(0,dataJson,env,url=f'{domainJY[env]}{path_snapshot}',nolog=1)
	try:
		curPrice=float(resp_snapshot['result']['basic']['curPrice'])
		logging.info(f'{code} 现价: {curPrice}')
		failed_reason='0'
	except:
		try:failed_reason=resp_snapshot['errorMsg']
		except:failed_reason='接口返回异常'
		curPrice=-9999
		logging.info(f'{resp_snapshot}')

	created_at=time.strftime('%Y-%m-%d %X')
	saveSQL=f"INSERT INTO interfaceTest_data.snapshot_curPrice_selfStock (created_at,stockCode,req_data,curPrice,failed_reason,resp_data) VALUES ('{created_at}','{code}','{formatSqlStr(dataJson)}',{curPrice},'{formatSqlStr(failed_reason)}','{formatSqlStr(resp_snapshot)}');"
	saveTodatabase(saveSQL)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def startTest(a,b):
		for item in allCode[a:b]:
			try:
				count_snapshot_curPrice(*item)
				# snapshot_timeShare(*item)
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