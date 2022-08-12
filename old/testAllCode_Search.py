import time
from common.database import queryCodelist
from common.tools import postReq,jsonpath_getAll,saveTodatabase,formatSqlStr
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('testAllcode_Search.Log'))

################################################################################################################
# 综合搜索及叫一夜搜索遍历测试

sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E'"
# sql="SELECT stock_code,stock_name FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' AND sec_type=1"
allCode=queryCodelist(0,0,sql,'test')

env='test'
from config import domainCMBI,assertObj

# mkTypeCodeDic={
# 	'NO':['XSHG.N','XSHG.MRI','XSHG.M','XSHG.KSH','XSHG.EU','XSHG.ESB','XSHG.EM.SF','XSHG.EM.LOF','XSHG.EM.ETF','XSHG.EM.CEF','XSHG.D','XSHG.DB.REPO','XSHG.DB.GBF','XSHG.DB.CPF','XSHG.DB.CCF','XSHE.N','XSHE.MRI','XSHE.M','XSHE.ESB','XSHE.EM.SF','XSHE.EM.LOF','XSHE.EM.ETF','XSHE.EM.CEF','XSHE.D','XHKG-M.DM','XHKG-M.DB.SARGOV','XHKG-M.DB.PRCGOV','XHKG-M.DB.M.HKD','XHKG-M.DB.M.CNY','XHKG-M.DB.HKMAE','XHKG-M.DB','XHKG-M.NS','XHKG-I.MRI','XUSI.MRI','XNYS.D','XNAS.D','XASE.D'],
# 	'YES':['XSHG.ESA.M','XSHG.ER','XSHE.ESA.SMSE','XSHE.ESA.M','XSHE.ESA.GEM','XHKG-M.TR.REIT','XHKG-M.TR.ETF','XHKG-M.TR','XHKG-M.RW.EW.CALL','XHKG-M.RW.DW.PUT','XHKG-M.RW.DW.CALL','XHKG-M.RW.CBBC.PUT','XHKG-M.RW.CBBC.CALL','XHKG-M.RW.IW','XHKG-M.RW','XHKG-M.ES','XBHK.ZZHY','XBHK.SGT','XBHK.LCG','XBHK.HSI','XBHK.HSHY','XBHK.HGT','XBHK.HCG','XBHK.GQG','XHKG-I.M','XHKG-G.RW.EW.CALL','XHKG-G.ES','XHKG-N.ES','XHKG-E.TR','XNYS.R','XNYS.M','XNYS.EUT','XNYS.EUF','XNYS.ES','XNYS.ADS','XNAS.R','XNAS.M','XNAS.EUT','XNAS.EUF','XNAS.ETN','XNAS.ES','XNAS.ADS','XASE.R','XASE.M','XASE.EUT','XASE.EUF','XASE.ETN','XASE.ES','XASE.ADS','XBUS.MX','XBUS.ZG']
# }
#########################################http###################################################################
# def search_center(codeInfo):
# 	path='/search-center/public/es/v2/searchFinInfoPageByValue'
# 	dataJson={
# 		'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",
# 		'finFrom':'0',
# 		'finSize':'20',
# 		'infoFrom':'0',
# 		'infoSize':'20',
# 		'searchValue':codeInfo[2],
# 	}
# 	respJson=postReq(0,dataJson,env,url=f'{domainCMBI[env]}{path}',mod='get',nolog=1)
# 	codeNames=jsonpath_getAll(respJson,'name')
# 	try:
# 		if codeInfo[1] in mkTypeCodeDic['NO']:
# 			assertObj.assertNotIn(codeInfo[3].strip(),codeNames)
# 		elif codeInfo[1] in mkTypeCodeDic['YES']:
# 			assertObj.assertIn(codeInfo[3].strip(),codeNames)
# 		else:
# 			raise AssertionError(f'{codeInfo} 不在范围内')
# 		logging.info(f'{codeInfo[2]} 测试通过')
# 	except AssertionError:
# 		logging.info(f'{codeInfo}\n返回数据: {respJson}\n断言失败:',exc_info=True)

# def search_center_trade(codeInfo):
# 	path='/gateway/order/stockNewSearch'
# 	dataJson={'inputSearch':codeInfo[2]}
# 	start=time.perf_counter()
# 	respJson=postReq(0,dataJson,env,url=f'{domainCMBI[env]}{path}',mod='post',nolog=1)
# 	elapsed=round((time.perf_counter()-start)*1000,2)
# 	codeNames=jsonpath_getAll(respJson,'productName')
# 	try:
# 		if codeInfo[1] in mkTypeCodeDic['NO']:
# 			assertObj.assertNotIn(codeInfo[3].strip(),codeNames)
# 			success,failed,reason=1,0,'不应搜索'
# 			logging.info(f'{codeInfo[2]} 测试通过 接口耗时: {elapsed} ms')
# 		elif codeInfo[1] in mkTypeCodeDic['YES']:
# 			assertObj.assertIn(codeInfo[3].strip(),codeNames)
# 			success,failed,reason=1,0,0
# 			logging.info(f'{codeInfo[2]} 测试通过 接口耗时: {elapsed} ms')
# 		else:
# 			success,failed,reason=0,1,f'{codeInfo} 不在范围内'
# 			elapsed,respJson=0,0
# 			logging.info(f'{codeInfo} 不在范围内')
# 	except AssertionError:
# 		try:reason=respJson['errorMsg']
# 		except KeyError:reason='返回数据异常'
# 		success,failed=0,1
# 		logging.info(f'{codeInfo} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=True)
	
# 	created_at=time.strftime('%Y-%m-%d %X')
# 	sql=f"INSERT INTO interfaceTest_data.stockNewSearch_1 (created_at,stockCode,path,req_data,success,failed,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{codeInfo[2]}_{codeInfo[3]}','{path}','{formatSqlStr(dataJson)}',{success},{failed},'{formatSqlStr(failed_reason)}',{elapsed},'{formatSqlStr(respJson)}');"
# 	saveTodatabase(sql)

##################################################################
# def search_center(stockcode,stockname):
# 	path='/search-center/public/es/v2/searchFinInfoPageByValue'
# 	dataJson={
# 		'traceLogId':f"FromZP{str(time.time()).replace('.','')}",
# 		'finFrom':'0',
# 		'finSize':'20',
# 		'infoFrom':'0',
# 		'infoSize':'20',
# 		'searchValue':stockcode,
# 	}
# 	respJson=postReq(0,dataJson,env,url=f'{domainCMBI[env]}{path}',mod='get',nolog=1)
# 	codeNames=jsonpath_getAll(respJson,'name')
# 	try:
# 		assertObj.assertIn(stockname.strip(),codeNames)
# 		logging.info(f'{stockcode} 测试通过')
# 		success=1;failed_reason='0'
# 	except AssertionError:
# 		success=0;failed_reason='断言失败'
# 		logging.info(f'{stockcode}\n返回数据: {respJson}\n断言失败:',exc_info=True)

# 	created_at=time.strftime('%Y-%m-%d %X')
# 	sql=f"INSERT INTO interfaceTest_data.search (created_at,keyword,path,req_data,success,failed_reason,resp_data) VALUES ('{created_at}','{stockcode}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson)}');"
# 	saveTodatabase(sql)

# def search_center_trade(stockcode,stockname):
# 	path='/gateway/order/stockNewSearch'
# 	dataJson={'inputSearch':stockcode}
# 	respJson=postReq(0,dataJson,env,url=f'{domainCMBI[env]}{path}',mod='post',nolog=1)
# 	codeNames=jsonpath_getAll(respJson,'productName')
# 	try:
# 		assertObj.assertIn(stockname.strip(),codeNames)
# 		success,failed_reason=1,0
# 		logging.info(f'{stockcode} 测试通过')
# 	except AssertionError:
# 		failed_reason='断言失败'
# 		success=0
# 		logging.info(f'{stockcode} 请求数据: {dataJson}\n返回数据: {respJson}\n断言失败:',exc_info=True)
	
# 	created_at=time.strftime('%Y-%m-%d %X')
# 	sql=f"INSERT INTO interfaceTest_data.search (created_at,keyword,path,req_data,success,failed_reason,resp_data) VALUES ('{created_at}','{stockcode}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson)}');"
# 	saveTodatabase(sql)

##################################################################
LZ_searchAble=['00001','00002','00003','00004','00005','00006','00011','00012','00016','00017','00019','00027','00066','00101','00119','00123','00135','00144','00148','00151','00152','00165','00168','00175','00200','00241','00257','00267','00268','00270','00285','00288','00291','00293','00322','00323','00338','00345','00347','00354','00358','00384','00386','00388','00390','00489','00522','00548','00552','00636','00656','00669','00670','00688','00694','00696','00700','00708','00728','00753','00762','00763','00772','00778','00780','00788','00799','00813','00823','00836','00853','00857','00867','00868','00874','00880','00881','00883','00902','00914','00916','00939','00941','00960','00966','00968','00981','00992','00998','01038','01044','01055','01066','01083','01088','01093','01099','01109','01113','01114','01128','01138','01157','01171','01177','01186','01193','01199','01211','01268','01288','01299','01313','01316','01317','01336','01337','01339','01347','01359','01398','01458','01548','01558','01579','01658','01766','01772','01776','01787','01789','01797','01800','01801','01810','01816','01818','01833','01876','01888','01896','01910','01918','01919','01928','01929','01951','01958','01972','01988','01995','01997','02007','02009','02013','02018','02020','02186','02196','02202','02208','02238','02269','02282','02313','02318','02319','02328','02331','02333','02338','02342','02357','02359','02382','02388','02600','02601','02607','02628','02669','02689','02727','02777','02799','02800','02822','02823','02840','02869','02883','02888','02899','03188','03311','03319','03320','03323','03328','03331','03333','03339','03383','03669','03690','03692','03759','03800','03883','03888','03898','03908','03918','03968','03969','03988','03993','03998','06030','06049','06060','06066','06098','06160','06169','06186','06808','06837','06862','06881','06886','08171','09618','09922','09988','09999','CEI','HSI','HSTECH',]

def search_LZ(stockcode):
	path='/finance-tools/public/lz/searchTarget'
	dataJson={
		'traceLogId':f"FromZP{str(time.time()).replace('.','')}",
		'keyWord':stockcode
	}
	respJson=postReq(0,dataJson,env,url=f'{domainCMBI[env]}{path}',mod='post',nolog=1)
	codeNames=jsonpath_getAll(respJson,'targetCode')
	try:
		if stockcode in LZ_searchAble:
			assertObj.assertIn(stockcode,codeNames)
		else:
			assertObj.assertNotIn(stockcode,codeNames)
		logging.info(f'{stockcode} 测试通过')
		success=1;failed_reason='0'
	except AssertionError:
		success=0;failed_reason='断言失败'
		logging.info(f'{stockcode}\n返回数据: {respJson}\n断言失败:',exc_info=True)

	created_at=time.strftime('%Y-%m-%d %X')
	sql=f"INSERT INTO interfaceTest_data.search_lz (created_at,keyword,path,req_data,success,failed_reason,resp_data) VALUES ('{created_at}','{stockcode}','{path}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(failed_reason)}','{formatSqlStr(respJson)}');"
	saveTodatabase(sql)


################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def start_search_center(a,b):
		for item in allCode[a:b]:
			try:
				# search_center(*item)
				# search_center_trade(*item)
				search_LZ(*item)
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
		t=threading.Thread(target=start_search_center,args=(splits[i],splits[i+1]))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')

'''
import os,json
os.chdir(r'')
fileName='聚源港美A股-0903.json'
sqlList=[]

with open(fileName,'r',encoding='utf-8') as file:
	allCode=json.load(file)
for item in allCode:
	stockName=item['stockName'].strip().replace("'","''")
	sql=f"INSERT INTO stock_quote VALUES ('{item['marketCode']}','{item['marketTypeCode']}','{item['stockCode']}','{stockName}');"
	sqlList.append(sql)

with open('HK_A_US.sql','w',encoding='utf-8') as file:
	file.write('\n'.join(sqlList))
'''
