import time
from common.database import queryCodelist,getDBconn,excuteSQL
from common.tools import postReq,saveTodatabase,formatSqlStr
from config import dataBaseInfo
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allcode_F10_HK_more_finance.Log'))

################################################################################################################
# 港股F10 相关接口美股码表遍历测试
from config import domainCMBI,assertObj

env='test'
sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' AND sec_type=3;"
allCode=queryCodelist(0,0,sql,'test')
# market_code= E B A N
logging.info(f'股票代码共 {len(allCode)} 个')


#########################################http###################################################################
def test_F10_HK_more_finance(stockCode):
	companyCode=getCompanyCode(stockCode)
	path='/doraemon/hkf10/more/finance'
	sectionId_list=['MORE_PROFIT','MORE_BALANCE','MORE_CASHFLOW']
	if companyCode:
		stockCode=f'E{stockCode}'
		dataJson={
			'companyCode':companyCode[0],
			'marketAndCode':stockCode,
			'moreFinanceNum':0,
			'stockName':companyCode[1],
		}
		for sectionId in sectionId_list:
			reason=None
			dataJson['sectionId']=sectionId
			_start=time.perf_counter()
			headerTraceLog=f'{stockCode}_{time.time()}'
			respJson=postReq(0,dataJson,0,url=f'http://0.0.0.0{path}',mod='get',nolog=1)
			elapsed=round((time.perf_counter()-_start)*1000,2)
			try:
				assertObj.assertTrue(respJson['success'])
				logging.info(f'{stockCode} 成功')
				success,reason=1,0
			except (AssertionError,KeyError,TypeError):
				success=0
				try:reason=respJson['errorMsg']
				except:reason='返回数据异常'
				if reason==None:
					logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}')
				else:
					logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=True)
			created_at=time.strftime('%Y-%m-%d %X')
			sql=f"INSERT INTO interfaceTest_data.f10_HK_more_finance (created_at,path,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
			saveTodatabase(sql)
	else:
		success=0;reason='查询CompanyCode失败';elapsed=0;respJson='';dataJson=''
		created_at=time.strftime('%Y-%m-%d %X')
		sql=f"INSERT INTO interfaceTest_data.f10_HK_more_finance (created_at,path,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
		saveTodatabase(sql)


def getCompanyCode(stockCode):
	sql=f"SELECT CompanyCode,SecuAbbr FROM JYDB.HK_SecuMain WHERE SecuCode='{stockCode}'"
	conn=getDBconn(dataBaseInfo[env]['host'],dataBaseInfo[env]['uname'],dataBaseInfo[env]['pword'],'mysql')
	result=excuteSQL(conn,sql,logit=0)
	try:
		return result[0]
	except TypeError:
		return None
################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def start_fuc(a,b):
		for code in allCode[a:b]:
			try:
				test_F10_HK_more_finance(code[0])
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

