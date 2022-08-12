import time
from common.tools import postReq
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_snapshot.Log'))

################################################################################################################
# snapshot 一万次
count=100000

env='test'
# market_code= E B A N
from config import domainJY,assertObj

#########################################http###################################################################
def snapshot(mk,code):
	path='/quote-query/quote/snapshot'
	dataJson={"marketCode":mk,"stockCode":code}
	dataJY=postReq(0,dataJson,env,url=f'{domainJY[env]}{path}',nolog=1)
	logging.info(f'返回数据 {dataJY}')
	# try:
	# 	assertObj.assertTrue(dataJY['success'])
	# 	assertObj.assertIsNotNone(dataJY['result'])
	# 	logging.info(f'snapshot {mk}{code} 测试通过')
	# except AssertionError:
	# 	logging.info(f'snapshot {mk}{code} 请求数据: {dataJson}\n返回数据: {dataJY}\n断言失败:',exc_info=True)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始,总计 {count} 次')
	###################################################################
	def start_fuc(a,b):
		for acc in range(count)[a:b]:
			try:
				snapshot("E",'00700')
			except:
				logging.error(f'{acc} 发生异常:',exc_info=True)

	def getSplit(data_len,ths):
		t=int(data_len/ths)
		splits=[i*t for i in range(ths+1)]
		splits[-1]=data_len
		return splits
	###################################################################
	import threading
	threads=[];thread_num=20
	splits=getSplit(count,thread_num)
	for i in range(thread_num):
		t=threading.Thread(target=start_fuc,args=(splits[i],splits[i+1]))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')