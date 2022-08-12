import time
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_reward.Log'))

################################################################################################################
# 抽奖概率验证



# env='dev'



#########################################http###################################################################
def reward_test():
	url='http://0.0.0.0/mkatoa/market/znq3/app/randomPrize'
	data={
	"promotionCode": "ZNQ3_2022-02-21-test2",
	"traceLogId": f"FromZP{str(time.time()).replace('.','')}"
	}
	respJson=postReq(0,data,0,url=f"{url}",mod='post',nolog=1)
	prizeKind=None
	prizeName=None
	prizeInfoId=None
	if respJson.get('success'):
		attendId=respJson['result']['attendId']
		try:
			prizeKind=respJson['result']['rewardInfo']['prizeKind']
			prizeName=respJson['result']['rewardInfo']['prizeName']
			prizeInfoId=respJson['result']['rewardInfo']['prizeInfoId']
			success,reason=1,0
		except:
			success,reason=0,'返回数据异常'

	else:
		success=0
		try:reason=respJson['errorMsg']
		except KeyError:reason='返回数据异常'

	created_at=time.strftime('%Y-%m-%d %X')
	sql=f"INSERT INTO interfaceTest_data.reward_test2 (created_at,req_data,success,prizeKind,prizeName,prizeInfoId,attendId,failed_reason,resp_data) VALUES ('{created_at}','{formatSqlStr(data)}','{success}','{prizeKind}','{prizeName}','{prizeInfoId}','{attendId}','{formatSqlStr(reason)}','{formatSqlStr(respJson)}');"
	saveTodatabase(sql)


################################################################################################################
if __name__ == '__main__':
	# reward_test()

	start=time.perf_counter()
	logging.info(f'测试开始')
	###################################################################
	def start_fuc():
		for n in range(100):
			try:
				logging.info(f'第 {n} 次请求')
				reward_test()
			except:
				logging.error(f'{n} 发生异常:',exc_info=True)

	###################################################################
	import threading
	threads=[];thread_num=10
	for i in range(thread_num):
		t=threading.Thread(target=start_fuc)
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')
