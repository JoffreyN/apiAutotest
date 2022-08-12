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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allcode_dividend.Log'))

################################################################################################################
# 分红派息 接口遍历测试
# from config import domainCMBI,assertObj
# from dividend_code import allCode

# env='dev'
# sql="SELECT stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' AND sec_type=3;"
# sql="SELECT stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;"
# allCode=queryCodelist(0,0,sql,'test')
# market_code= E B A N
# logging.info(f'股票代码共 {len(allCode)} 个')


#########################################http###################################################################
def dividendCenter_pageList():
	host='http://0.0.0.0'
	path='/doraemon/dividendCenter/pageList'

	market_dict={'E':'港股','N':'美股','A':'沪深'}
	type_dict={0:'全部',1:'年度',2:'中期',3:'季度',4:'月度',5:'其他'}

	for market in ['E','N','A']:
		for year in range(2016,2022):
			for t in range(6):
				pageIndex=1
				flag=1
				while flag:
					dataJson={"market":market,"pageIndex":pageIndex,"pageSize":20,"type":t,"traceLogId":f"FromZP{str(time.time()).replace('.','')}","year":year,"sortType":"1","sortField":"3"}
					describes=f'{market} {year}年 {type_dict[t]} 第{pageIndex}页'
					logging.info(describes)

					_start=time.perf_counter()
					respJson=postReq(0,dataJson,0,url=f"{host}{path}",mod='post',nolog=1)
					# print(respJson)
					elapsed=round((time.perf_counter()-_start)*1000,2)

					itemList=respJson.get('result').get('dividendCenterPageItemList')
					flag=len(itemList) if itemList else 0

					if respJson.get('success'):
						if flag:
							try:
								_templist=[]
								for item in itemList:
									_templist.append(f"{item['stockCode']}_{item['dmpublDate'].split()[0]}")
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
					sql=f"INSERT INTO interfaceTest_data.dividend_pageList2 (created_at,path,describes,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{describes}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
					# print(sql)
					saveTodatabase(sql)

def dividendCenter_detailPageList(market_stockCode):
	market,stockCode=market_stockCode[0],market_stockCode[1:]
	host='http://0.0.0.0'
	path='/doraemon/dividendCenter/detailPageList'
	market_dict={'E':'港股','N':'美股','A':'沪深'}
	pageIndex=1
	flag=1
	while flag:
		dataJson={"market":market,"pageIndex":pageIndex,"pageSize":20,"stockCode":stockCode,"traceLogId":f"FromZP{str(time.time()).replace('.','')}"} 
		describes=f'{market} {stockCode} 第{pageIndex}页'
		logging.info(describes)

		_start=time.perf_counter()
		respJson=postReq(0,dataJson,0,url=f"{host}{path}",mod='post',nolog=1)
		# print(respJson)
		elapsed=round((time.perf_counter()-_start)*1000,2)

		itemList=respJson.get('result').get('dividendCenterDetailPageItemList')
		flag=len(itemList) if itemList else 0

		if respJson.get('success'):
			if flag:
				try:
					_templist=[]
					for item in itemList:
						_templist.append(f"{item['statement']}_{item['dmpublDate'].split()[0]}")
					if len(_templist)==len(set(_templist)):success,reason=1,0
					else:success,reason=0,f'同一公告日有重复数据 {_templist}'
				except:
					success,reason=0,'返回数据异常(股票代码或公告日)'
			else:
				success,reason=0,'返回数据为空'
		else:
			success=0
			try:reason=respJson['errorMsg']
			except KeyError:reason='返回数据异常'
		pageIndex+=1

		created_at=time.strftime('%Y-%m-%d %X')
		sql=f"INSERT INTO interfaceTest_data.dividend_pageList_detail2 (created_at,path,describes,req_data,success,failed_reason,elapsed,resp_data) VALUES ('{created_at}','{path}','{describes}','{formatSqlStr(dataJson)}',{success},'{formatSqlStr(reason)}',{elapsed},'{formatSqlStr(respJson)}');"
		# print(sql)
		saveTodatabase(sql)
		if 0<flag<20:break

################################################################################################################
if __name__ == '__main__':
	dividendCenter_pageList()

	# start=time.perf_counter()
	# logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	# ###################################################################
	# def start_fuc(a,b):
	# 	for code in allCode[a:b]:
	# 		try:
	# 			dividendCenter_detailPageList(code)
	# 		except:
	# 			logging.error(f'{code} 发生异常:',exc_info=True)

	# def getSplit(data_len,ths):
	# 	t=int(data_len/ths)
	# 	splits=[i*t for i in range(ths+1)]
	# 	splits[-1]=data_len
	# 	return splits
	# ###################################################################
	# import threading
	# threads=[];thread_num=50
	# splits=getSplit(len(allCode),thread_num)
	# for i in range(thread_num):
	# 	t=threading.Thread(target=start_fuc,args=(splits[i],splits[i+1]))
	# 	threads.append(t)
	# 	t.start()
	# for t in threads:
	# 	t.join()
	# ###################################################################
	# t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	# logging.info(f'测试结束 耗时: {t}\n\n\n')
