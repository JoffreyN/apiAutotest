import time,sys
from functools import reduce
from jsonpath import jsonpath
from common.tools import postReq
from common.database import getDBconn,excuteSQL
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('testIqdii.Log'))

################################################################################################################
# 捷利行情接入服务升级功能可用性测试
from config import domainCMBI,assertObj,dataBaseInfo
env='test'

# /gateway2/stock/stockInfo F10，len(respJson["result"]["tabs"])>0
# 0 /gateway2/stock/kLine K线,   len(respJson["result"]["list"]>0,list每个字段不为0)
# 0 /gateway2/stock/realTime 分时图，len(respJson["result"]>0,均线>0)
# /gateway2/stock/orderbook 买卖档行情，（有档位）
# /gateway2/stock/quote 基础报价。 
# 0 /gateway2/stock/home 港股市场行情首页
# 0 /gateway2/stock/industryRank 行业板块排行  
# 0 /gateway2/stock/industry 行业涨幅排行。 （长度大于0）
# 0 /gateway2/stock/rank 市场涨跌幅排行。 （长度大于0）
# /gateway2/stock/getHotStock 查询热门股。 （长度要三个，）
# /gateway2/stock/stockpicks 查询股票详情。（加上指数，然后要求返回的数据里面必须有指数，且数据不为0）
################################################################################################################
def main(path):
	url=f'{domainCMBI[env]}{path}'
	if path=='/gateway2/stock/stockInfo':
		dataJson={'secuCode':'E00700'}
	elif path=='/gateway2/stock/kLine':
		dataJson={'code':'E00700','ktype':'1','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/realTime':
		dataJson={'code':'E00700','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/orderbook':
		dataJson={'code':'E00700','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/quote':
		dataJson={'code':'E00700','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/home':
		dataJson={'marketType':'1','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/industryRank':
		dataJson={'marketType':'1','asc':'1','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/industry':
		dataJson={'marketType':'1','asc':'1','code':'202001','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/rank':
		dataJson={'marketType':'1','para':'zdf','asc':'1','code':'210002','traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/getHotStock':
		dataJson={'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}"}
	elif path=='/gateway2/stock/stockpicks':
		# dataJson={'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",'list':[]}
		dataJson={'traceLogId':f"FromZP{time.strftime('%Y%m%d%H%M%S')}",'list':['A399001','B1A0001','A399300','E01249','E00700','E00513','E08030','E08356','E08613','A300760','B600519']}
	start=time.perf_counter()
	respJson=postReq(0,dataJson,0,url=url,mod='post',nolog=1)
	elapsed=round((time.perf_counter()-start)*1000,2)
	try:
		if path=='/gateway2/stock/stockInfo':
			assertObj.assertGreater(len(respJson["result"]["tabs"]),0)
		elif path=='/gateway2/stock/kLine':
			assertObj.assertGreater(len(respJson["result"]["list"])*reduce(lambda x,y:x*y,(len(item) for item in respJson["result"]["list"])),0)
		elif path=='/gateway2/stock/realTime':
			assertObj.assertGreater(len(respJson["result"]),0)
		elif path=='/gateway2/stock/orderbook':
			assertObj.assertGreater(len(respJson["result"]["orderbook"]['ask'])*len(respJson["result"]["orderbook"]['bid']),0)
		elif path=='/gateway2/stock/quote':
			assertObj.assertGreater(float(jsonpath(respJson,'$..price')[0]),0)
		elif path=='/gateway2/stock/home':
			pass
		elif path=='/gateway2/stock/industryRank':
			pass
		elif path=='/gateway2/stock/industry':
			assertObj.assertGreater(len(respJson["result"]['list']),0)
		elif path=='/gateway2/stock/rank':
			assertObj.assertGreater(len(respJson["result"]['list']),0)
		elif path=='/gateway2/stock/getHotStock':
			assertObj.assertGreater(len(respJson["result"]),3)
		elif path=='/gateway2/stock/stockpicks':
			assertObj.assertGreater(reduce(lambda x,y:x*y,map(float,jsonpath(respJson,'$..xj'))),0)
		assertObj.assertTrue(respJson['success'])
		success,failed,reason=1,0,0
		logging.info(f'{path} 测试通过 接口耗时: {elapsed} ms')
	except (AssertionError,TypeError):
		success,failed,reason=0,1,respJson['errorMsg']
		if not reason:reason='返回数据异常'
		logging.info(f'{path} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}\n断言失败:',exc_info=1)
	# logging.info(f'debug: {path} 请求数据: {dataJson}\n返回数据(耗时 {elapsed} ms): {respJson}')
	saveTodatabase(path,success,failed,reason,elapsed)

def saveTodatabase(path,success,failed,reason,elapsed):
	created_at=time.strftime('%Y-%m-%d %X')
	date=time.strftime('%m-%d %H')
	sql=f"INSERT INTO test.jieli_updateServer (created_at,path,success,failed,failed_reason,elapsed,date) VALUES ('{created_at}','{path}',{success},{failed},'{reason}',{elapsed},'{date}');"
	conn=getDBconn(dataBaseInfo['dev']['host'],dataBaseInfo['dev']['uname'],dataBaseInfo['dev']['pword'],'mysql')
	excuteSQL(conn,sql,0)

def countdown(t):
	while t:
		sys.stdout.write(f'{t} 秒后开始下一次测试\r')
		sys.stdout.flush()
		t-=1
		time.sleep(1)

################################################################################################################
if __name__ == '__main__':
	pathList=[
		# '/gateway2/stock/stockInfo',
		# '/gateway2/stock/kLine',
		'/gateway2/stock/realTime',
		'/gateway2/stock/orderbook',
		'/gateway2/stock/quote',
		# '/gateway2/stock/home',
		# '/gateway2/stock/industryRank',
		# '/gateway2/stock/industry',
		# '/gateway2/stock/rank',
		# '/gateway2/stock/getHotStock',
		'/gateway2/stock/stockpicks',
	]
	n=1
	while 1:
		logging.info(f'开始第 {n} 次测试')
		for path in pathList:main(path)
		n+=1
		countdown(600)