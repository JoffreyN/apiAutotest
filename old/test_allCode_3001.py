import time
from common.database import queryCodelist
from common.tools import saveTodatabase,formatSqlStr
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allCode_3001.Log'))

################################################################################################################
# 此脚本 遍历所有股票订阅数据

env='test'
sql="SELECT market_code,stock_code FROM test_quote_sync.t_stock_info WHERE enable_search=1 AND market_code='E' LIMIT 10"
# allCode=queryCodelist(0,0,sql,env)
allCode=[('E','00700')]

# allCode=queryCodelist(0,0,"SELECT market_code,stock_code FROM dev_quote_sync.t_stock_info WHERE enable_search=1 AND (market_code='E' OR market_code='B' OR  market_code='A') order by rand() LIMIT 100;")
# market_code= E B A N
from config import wsHost

from websocket import create_connection
from client import send_msg,init_req,sub_req,parseData
#########################################websocket###################################################################
def send_sub(market,stockcode):
	wsConn=create_connection(wsHost[env])
	uname,pword='****','****'
	# token=getToken(uname,pword,env)['token']
	token='E5DDB73C7F40B484CDD3945966CF6583'
	# logging.info(f'InitConnect 发送数据: {uname} {token}')
	code,respjson=send_msg(wsConn,1001,init_req(uname,token),1)
	# logging.info(f'{code} init响应: {respjson}')

	# SubType_Snapshot_Full = 1; // 基础报价 (包含快照 + 分时 + 五档)
	# SubType_Snapshot_Basic = 2; // 基础报价简版（用于自选股）
	# SubType_OrderBook = 3; // 摆盘
	# for i in range(3):
	data={
		"secuList":[{"market":market,"code":stockcode}],
		"subTypeList":[1],
		"regPushRehabTypeList":[0],
		"isSubOrUnSub":True,
		"isFirstPush":True,
		"isUnsubAll":False
	}
	logging.info(f'send_sub 发送: {data}')
	code,respjson=send_msg(wsConn,3001,sub_req(data),getRecv=1)
	logging.info(f"收到数据: {code} {respjson}")

	logging.info(f"等待接收数据")
	recv=wsConn.recv()# 如果服务器没有数据返回，会一直卡在这里 多线程也无效 直至连接超时断开
	code,resp=parseData(recv)
	dataJson=json.loads(pbjson.pb2json(resp))
	logging.info(f"收到数据: {code} {dataJson}")

	wsConn.close()



################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计代码 {len(allCode)} 个')
	###################################################################
	for item in allCode:
		try:
			send_sub(*item)
		except:
			logging.error(f'{item} 发生异常:',exc_info=True)

	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')