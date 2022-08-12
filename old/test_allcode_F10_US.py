import time
from common.database import queryCodelist,getInnerCompanyCode
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
__s=time.strftime('%Y%m%d%H')
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler(f'test_allUScode_F10_{__s}.Log'))

################################################################################################################
# 美股F10 相关接口美股码表遍历测试
from config import domainCMBI,assertObj,dataBaseInfo
# /dcus/brief/basic  获取简况-基本资料
# /dcus/brief/companyMovement  获取简况-公司行动
# /dcus/brief/managementTeam  获取简况-管理团队
# /dcus/brief/shareHolder  获取简况-股本股东
# /dcus/finance  获取财务tab
# /dcus/finance/moreBalance  获取更多资产负债表数据
# /dcus/finance/moreCashFlow  获取更多现金流量表数据
# /dcus/finance/moreMainBusiness  获取财务-更多主营构成
# /dcus/finance/moreProfit  获取更多利润表数据
# /dcus/getBasicRes  获取基本证券代码相关信息

env='test'
sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='N' AND sec_type=3;"
# sql="SELECT stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;"

allCode=queryCodelist(0,0,sql,env)
# market_code= E B A N
# allCode=(('CAG',),('VMC',),('DHR',),('ON',),('KMI',),('AGMH',),('ETN',),('TXT',),('SECO',),('DXC',),('WYND',),('LMT',),('GWW',),('XOM',),)
# allCode=(('ACEVU'),)

commonPath=[
	'/dcus/brief/basic',
	'/dcus/getBasicRes',
	'/dcus/brief/companyMovement',
	'/dcus/brief/managementTeam',
	'/dcus/brief/shareHolder',
	'/dcus/finance',
	'/dcus/finance/moreBalance',
	'/dcus/finance/moreCashFlow',
	'/dcus/finance/moreMainBusiness',
	'/dcus/finance/moreProfit',
	'/dcus/announcements',
	'/dcus/sellShort',
]
#########################################http###################################################################
def test_UScode_F10(stockCode):
	stockCode,innerCode,companyCode=getInnerCompanyCode(stockCode)
	flag=1 if innerCode and companyCode else 0
	for path in commonPath:
		if path in ['/dcus/brief/basic','/dcus/getBasicRes','/dcus/sellShort']:
			dataJson={'stockCode':stockCode}
		elif path in ['/dcus/brief/companyMovement','/dcus/announcements']:
			dataJson={'innerCode':innerCode}
		elif path in ['/dcus/brief/managementTeam','/dcus/finance/moreBalance','/dcus/finance/moreCashFlow','/dcus/finance/moreProfit']:
			dataJson={'companyCode':companyCode}
		elif path in ['/dcus/finance/moreMainBusiness']:
			dataJson={'stockCode':stockCode,'companyCode':companyCode}
		elif path in ['/dcus/brief/shareHolder']:
			dataJson={'innerCode':innerCode,'companyCode':companyCode}
		elif path in ['/dcus/finance']:
			dataJson={'stockCode':stockCode,'companyCode':companyCode,'innerCode':innerCode}

		headerTraceLog=str(time.time())
		if flag:
			start=time.perf_counter()
			respJson=postReq(0,dataJson,0,url=f'{domainCMBI[env]}/doraemon{path}',mod='get',nolog=1,headerTraceLog=headerTraceLog)
			elapsed=round((time.perf_counter()-start)*1000,2)
			try:
				assertObj.assertTrue(respJson['success'])
				logging.info(f'{path} {stockCode} 测试通过 接口耗时: {elapsed} ms')
				success,reason=1,0
			except AssertionError:
				success=0;reason='断言失败'
				logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=True)
			except KeyError:
				success=0;reason='返回数据异常'
				logging.info(f'{path} {stockCode} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n返回数据异常:',exc_info=True)

		else:
			success,reason=0,'查询InnerCode、companyCode失败'
			respJson='';elapsed=0
		created_at=time.strftime('%Y-%m-%d %X')
		h=int(time.strftime('%H'))
		tableName='f10_US' if h<=12 else 'f10_US_1'
		sql=f"INSERT INTO interfaceTest_data.{tableName} (created_at,stockCode,path,headerTraceLog,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{stockCode}','{path}','{headerTraceLog}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
		saveTodatabase(sql)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def start_fuc(a,b):
		for code in allCode[a:b]:
			try:
				test_UScode_F10(code[0])
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
