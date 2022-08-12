import time
from common.database import getDBconn,excuteSQL
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_importantEvents.Log'))

################################################################################################################
# importantEvents 根据市场+证券代码获取重大事件 uat 及test环境数据对比


sql1="SELECT A.EXDATE exDate, A.SCHEMEDESC schemeDesc, A.SECURITYCODE stockCode FROM dcmg.USCO_IA_DIVIDEND A LEFT JOIN dcmg.CDSY_SECUCODE B ON A.SECINNERCODE = B.SECINNERCODE WHERE A.EXDATE BETWEEN '2021-09-15 00:00:00.0' AND '2021-09-22 00:00:00.0' AND A.EISDEL = '0' ORDER BY A.EXDATE DESC;"
sql2="SELECT A.EXREDATE exreDate, A.FCDATE firstChangeDate, A.SCDATE secondChangeDate, A.SECINNERCODE innerCode, B.SECURITYCODE stockCode, A.RADATE FROM dcmg.USCO_FN_EXDATE A LEFT JOIN dcmg.CDSY_SECUCODE B ON A.SECINNERCODE = B.SECINNERCODE WHERE ISNULL(A.RADATE)  AND (A.SCDATE BETWEEN '2021-09-15 00:00:00.0' AND '2021-09-22 00:00:00.0' OR A.FCDATE BETWEEN '2021-09-15 00:00:00.0' AND '2021-09-22 00:00:00.0' OR A.EXREDATE BETWEEN '2021-09-15 00:00:00.0' AND '2021-09-22 00:00:00.0');"

conn=getDBconn('0.0.0.0','****','******','mysql')
result1=excuteSQL(conn,sql1,0)

conn=getDBconn('0.0.0.0','****','******','mysql')
result2=excuteSQL(conn,sql2,0)

allCode=[('N',i[2]) for i in result1]+[('N',j[4]) for j in result2]
# print(allCode)

from config import domainCMBI

#########################################http###################################################################
def importantEvents(mk,code):
	path='/doraemon/hkf10/importantEvents'
	dataJson={"marketAndCodes": [f"{mk}{code}"]}
	logging.info(f'请求数据: {dataJson}')
	respJson_test=postReq(0,dataJson,'test',url=f'{domainCMBI["test"]}{path}',nolog=1)
	respJson_uat=postReq(0,dataJson,'uat',url=f'{domainCMBI["uat"]}{path}',nolog=1)
	if respJson_test==respJson_uat:
		success=1;failed_reason='0'
	else:
		success=0;failed_reason='对比不一致'

	created_at=time.strftime('%Y-%m-%d %X')

	saveSQL=f"INSERT INTO interfaceTest_data.importantEvents (created_at,path,req_data,success,failed_reason,respData_test,respData_uat) VALUES ('{created_at}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson_test)}','{formatSqlStr(respJson_uat)}');"
	saveTodatabase(saveSQL)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始,总计代码 {len(allCode)} 个')
	###################################################################
	def startTest(a,b):
		for item in allCode[a:b]:
			try:
				importantEvents(*item)
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