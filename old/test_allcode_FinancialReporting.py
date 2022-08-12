import time,json
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allcode_FinancialReporting.Log'))

################################################################################################################
# 财报中心 接口遍历测试 
# from config import domainCMBI,assertObj
from financialReporte_code import allCode

# env='dev'
# sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' AND sec_type=3;"
# sql="SELECT stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;"
# allCode=queryCodelist(0,0,sql,'test')
# market_code= E B A N
# logging.info(f'股票代码共 {len(allCode)} 个')


#########################################http###################################################################
def FinancialReporting():
	host='http://0.0.0.0'
	path_dict={'E':'/doraemon/financialReportHk/performance','N':'/doraemon/financialReportUs/performance','A':'/doraemon/financialReportHs/performance'}

	market_dict={'E':'港股','N':'美股','A':'沪深'}
	type_dict={'全部':'','年度':'year','中期':'middle','季度':'quarter'}

	for market in ['E','N','A']:
		path=path_dict[market]
		for year in range(2016,2022):
			for k,v in type_dict.items():
				pageIndex=1
				flag=1
				while flag:
					dataJson={'pageNo':pageIndex,'pageSize':'20','financialYear':year,'periodicalNum':v,'sort':'desc','sortField':'publicDate','traceLogId':f"FromZP{str(time.time()).replace('.','')}"}

					describes=f'{market} {year}年 {k} 第{pageIndex}页'
					logging.info(describes)

					_start=time.perf_counter()
					respJson=postReq(0,dataJson,0,url=f"{host}{path}",mod='get',nolog=1)
					# print(respJson)
					elapsed=round((time.perf_counter()-_start)*1000,2)

					itemList=respJson.get('result')
					flag=len(itemList) if itemList else 0

					if respJson.get('success'):
						if flag:
							try:
								_templist=[]
								for item in itemList:
									_templist.append(f"{item['securityCode']}_{item['financialYear']}_{item['timeTypeCode']}")
								if len(_templist)==len(set(_templist)):success,reason=1,0
								else:success,reason=0,f'同一股票同一天内有超过1条数据 {_templist}'
							except:
								success,reason=0,'返回数据异常(股票代码或公告日)'
						else:
							success,reason=1,0
					else:
						success=0
						try:reason=respJson['errorMsg']
						except KeyError:reason='返回数据异常'
					pageIndex+=1	
					created_at=time.strftime('%Y-%m-%d %X')
					sql=f"INSERT INTO interfaceTest_data.financialreporting (created_at,path,describes,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{describes}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
					# print(sql)
					saveTodatabase(sql)

def FinancialReporting_detail(market_stockCode):
	host='http://0.0.0.0'
	path_dict={'E':'/doraemon/financialReportHk/performance','N':'/doraemon/financialReportUs/performance','A':'/doraemon/financialReportHs/performance'}
	market_dict={'E':'港股','N':'美股','A':'沪深'}
	path=path_dict[market_stockCode[0]]
	pageIndex=1;pageSize=100
	flag=1
	while flag:
		dataJson={'pageNo':pageIndex,'pageSize':pageSize,'sort':'desc','sortField':'publicDate','innerCodeList':market_stockCode,'traceLogId':f"FromZP{str(time.time()).replace('.','')}"}
		describes=f'{market_stockCode} 第{pageIndex}页'
		logging.info(describes)

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=f"{host}{path}",mod='get',nolog=1)
		# print(respJson)
		elapsed=round((time.perf_counter()-_start)*1000,2)

		itemList=respJson.get('result')
		flag=len(itemList) if itemList else 0

		if respJson.get('success'):
			if flag:
				result_dict=getresult_dict(itemList)
				reason1=checkYoy(result_dict,types='营收')
				reason2=checkYoy(result_dict,types='净利润')
				reason=reason1+reason2
				success=0 if '差值大于0.01' in reason else 1
				# try:
				# 	_templist=[]
				# 	for item in itemList:
				# 		_templist.append(f"{item['securityCode']}_{item['financialYear']}_{item['timeTypeCode']}")
				# 	if len(_templist)==len(set(_templist)):success,reason=1,0
				# 	else:success,reason=0,f'重复数据 {_templist}'
				# except:
				# 	success,reason=0,'返回数据异常(股票代码或财报年或timeTypeCode)'
			else:
				success,reason=0,'返回数据为空'
		else:
			success=0
			try:reason=respJson['errorMsg']
			except KeyError:reason='返回数据异常'
		pageIndex+=1

		created_at=time.strftime('%Y-%m-%d %X')
		sql=f"INSERT INTO interfaceTest_data.financialreporting_detail3 (created_at,path,describes,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{describes}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
		# print(sql)
		saveTodatabase(sql)
		if 0<flag<pageSize:break

def getresult_dict(result):
	result_dict={}
	for item in result:
		financialYear=item.get('financialYear')
		timeTypeCode=item.get('timeTypeCode')
		revenue=item.get('revenue')
		revenueYoy=item.get('revenueYoy')
		profit=item.get('profit')
		profitYoy=item.get('profitYoy')
		
		if financialYear not in result_dict.keys():result_dict[financialYear]={}
		result_dict[financialYear][timeTypeCode]={'revenue':revenue,'revenueYoy':revenueYoy,'profit':profit,'profitYoy':profitYoy}
	return result_dict

def checkYoy(result_dict,types='营收'):
	reason=''
	key='revenue' if types=='营收' else 'profit'
	for year,financial in result_dict.items():
		for timeTypeCode,revenueProfit_dict in financial.items():
			data=revenueProfit_dict[key]
			dataYoy=revenueProfit_dict[f'{key}Yoy']
			
			lastyear=str(int(year)-1)
			try:
				lastyear_data=result_dict[lastyear][timeTypeCode][key]
			except KeyError:
				lastyear_data=None
			try:
				my_dataYoy=round((float(data)-float(lastyear_data))/abs(float(lastyear_data)),6)
			except TypeError:
				my_dataYoy=None
			except ZeroDivisionError:
				reason=reason+f'{lastyear} {timeTypeCode} {types}数据为{lastyear_data} 被除数为0;'
				continue

			
			if my_dataYoy and dataYoy:
				if abs(float(my_dataYoy)-float(dataYoy))>0.01:
					reason=reason+f'{year} {timeTypeCode} {types}同比计算差值大于0.01,计算结果: {my_dataYoy} ,接口返回: {dataYoy};'
			elif my_dataYoy!=dataYoy:
					reason=reason+f'{year} {timeTypeCode} {types}同比结果不一致,计算结果: {my_dataYoy} ,接口返回: {dataYoy};'

	return reason


################################################################################################################
if __name__ == '__main__':
	# FinancialReporting()

	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	def start_fuc(a,b):
		for code in allCode[a:b]:
			try:
				FinancialReporting_detail(code)
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
