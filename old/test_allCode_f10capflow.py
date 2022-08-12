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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allCode_f10capflow.Log'))

################################################################################################################
# f10 资金tab

env='test'
sql="SELECT market_code,stock_code FROM test_quote_sync.t_stock_info WHERE sec_type=3 AND (market_code='N' OR market_code='A' OR market_code='B' OR  market_code='E') AND enable_search=1"
# allCode=queryCodelist(0,0,sql,env)
allCode=[('E','00376'),('E','02699'),('N','VCYT'),('N','ADMS'),('N','CNK'),('N','RC'),('E','00520'),('N','RCMT'),('E','02700'),('N','USOI'),('N','ADPT'),('N','RBA'),('N','CNNE'),('E','00521'),('N','LIFE'),('N','VEON'),('N','IBTX'),('N','RCB'),('N','CMSC'),('E','00522'),('N','FTAC'),('N','ADTN'),('N','FRHC'),('N','RFP'),('N','FULC'),('N','VNDA'),('N','CPS'),('N','ADXS'),('E','00546'),('E','00099'),('N','GSBD'),('N','AEM'),('N','CBOE'),('N','TD'),('N','SMTX'),('E','01907'),('N','USB-R'),('N','SFTW.UN'),('N','J'),('N','SND'),('E','01908'),('N','ATMR.UN'),('N','NFG'),]

from config import domainJY,assertObj

#########################################http###################################################################
def capflow(mk,code):
	path='/quote-query/qot/capflow'
	dataJson={"marketCode":mk,"stockCode":code,"traceLogId":f"FromZP{str(time.time()).replace('.','')}"}
	logging.info(f'请求数据: {dataJson}')
	respJson=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	if respJson['success']:
		success=1;failed_reason='0'
	else:
		success=0
		try:failed_reason=respJson['errorMsg']
		except:failed_reason='接口返回异常'

	created_at=time.strftime('%Y-%m-%d %X')
	saveSQL=f"INSERT INTO interfaceTest_data.f10_capflow (created_at,req_data,success,failed_reason,resp_data) VALUES ('{created_at}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson)}');"
	saveTodatabase(saveSQL)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始,总计代码 {len(allCode)} 个')
	###################################################################
	def startTest(a,b):
		for item in allCode[a:b]:
			try:
				capflow(*item)
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