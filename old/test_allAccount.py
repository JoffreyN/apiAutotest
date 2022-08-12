import time,requests
from common.tools import postReq,jsonpath_getOne,saveTodatabase,formatSqlStr
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
logging.getLogger().addHandler(HandlerFactory.get_rotating_file_handler('test_allAccount.Log'))

################################################################################################################
# 遍历账户持仓及购买力接口

env='uat'
from config import domainCMBI

accountPool={
	'test':["918272","M918272","918275","M918275","918276","M918276","918277","M918277","918278","M918278","918279","M918279","918280","M918280","918281","M918281","918282","M918282","918283","M918283","918287","M918287","918288","M918288","918289","M918289","918290","M918290","918291","M918291","918292","M918292","918293","M918293","918295","M918295","918296","M918296","918297","M918297","918298","M918298","918299","M918299","918300","M918300","918301","M918301","918302","M918302","918303","M918303","918305","M918305","918306","M918306","918307","M918307","918308","M918308","918309","M918309","918310","M918310","290717","M290717","290718","M290718","290719","M290719","290720","M290720","290721","M290721","290723","M290723","290725","M290725","290726","M290726","290727","M290727","290728","M290728","290729","M290729","290730","M290730","290732","M290732","290733","M290733","290735","M290735","290736","M290736","290738","M290738","290750","M290750",],
	'uat':["702787","M702787","702833","M702833","702890","M702890","702892","M702892","702893","M702893","702895","M702895","702896","M702896","702897","M702897","702899","M702899","702900","M702900","702901","M702901","702902","M702902","702905","M702905","702906","M702906","291596","M291596","291598","M291598","291599","M291599","291600","M291600","291601","M291601","291602","M291602","291603","M291603","702909","M702909","702910","M702910","702930","M702930","702931","M702931","702932","M702932","702933","M702933","702935","M702935","291628","M291628","291629","M291629","291630","M291630","291631","M291631","291632","M291632","703112","M703112","703113","M703113","703115","M703115","703116","M703116","703117","M703117","703118","M703118","703119","M703119","703120","M703120","703121","M703121","703122","M703122","703123","M703123","703125","M703125","703126","M703126","703127","M703127","703128","M703128","703129","M703129","703130","M703130","703131","M703131","703132","M703132","703133","M703133","703135","M703135","703136","M703136","703137","M703137","703138","M703138","703139","M703139","703150","M703150","703151","M703151","703152","M703152","703153","M703153","703155","M703155","703156","M703156","703157","M703157","703158","M703158","703159","M703159","703160","M703160","703161","M703161","703162","M703162","703163","M703163","703165","M703165","703166","M703166","703168","M703168","703169","M703169","703170","M703170","703171","M703171","703172","M703172","703173","M703173","703175","M703175","703176","M703176","703177","M703177","703178","M703178","703179","M703179","703180","M703180","703181","M703181","703182","M703182","703183","M703183","703185","M703185","703186","M703186","703187","M703187","703188","M703188","703189","M703189","703190","M703190","703191","M703191","703192","M703192","703193","M703193","703195","M703195","703196","M703196","703197","M703197","703198","M703198","703199","M703199","703200","M703200","703201","M703201","703202","M703202","703203","M703203","703205","M703205","703206","M703206","703207","M703207","703208","M703208","703209","M703209","703210","M703210","703211","M703211","703212","M703212","703213","M703213","703215","M703215","703217","M703217","703218","M703218","703219","M703219","703220","M703220","703221","M703221","703222","M703222","703223","M703223","703225","M703225","703226","M703226","703227","M703227","703228","M703228",]
}

################################################################################################################
def getSession(uname,pword):
	url=f'{domainCMBI[env]}/app/user/login'
	key={'account':uname,'password':pword}
	head={'Connection':'close','Content-Type':'application/x-www-form-urlencoded'}
	resp=requests.post(url,headers=head,data=key)
	respJson=resp.json()
	# logging.info(f'返回数据: {respJson}')
	session={
		"token":jsonpath_getOne(respJson,'token',dataType='str',nan='0'),
		"sessionId":jsonpath_getOne(respJson,'sessionid','str'),
		"accountId":jsonpath_getOne(respJson,'accountid','str'),
		"acctType":jsonpath_getOne(respJson,'acctype','str'),
		"aecode":jsonpath_getOne(respJson,'aecode','str'),
		"marginMax":jsonpath_getOne(respJson,'margin_max','str'),
	}
	if session['token']=='0':
		logging.info(f'{uname} 登录失败: {respJson} ')
		return 0,respJson
	else:
		return 1,session

def queryAccountAndHold(uname,pword):
	status,session=getSession(uname,pword)
	if status:
		path1='/gateway/order/queryAccountAndHold'
		respJson1=postReq(0,session,env,url=f'{domainCMBI[env]}{path1}',mod='post',nolog=1)
		logging.info(f'{uname} 返回持仓数据: {respJson1}')

		path2='/gateway/order/stockDealing'
		respJson2=[]
		for item in [("HK","00700"),("US","BILI"),("SHA","600519")]:
			reqData={"marketCode":item[0],"productNo":item[1]}
			__respjson=postReq(0,dict(session,**reqData),env,url=f'{domainCMBI[env]}{path2}',mod='post',nolog=1)
			logging.info(f'{uname} 返回 {item[1]} 购买力数据: {__respjson}')
			respJson2.append(__respjson)
		success,failed_reason=1,'0'
	else:
		respJson1,respJson2='0','0'
		success,failed_reason=0,session['message']

	created_at=time.strftime('%Y-%m-%d %X')
	sql=f"INSERT INTO interfaceTest_data.account_stockdealing_uat (created_at,account,success,failed_reason,money_hold,stockDealing) VALUES ('{created_at}','{uname}','{success}','{formatSqlStr(failed_reason)}','{formatSqlStr(respJson1)}','{formatSqlStr(respJson2)}');"
	saveTodatabase(sql)

################################################################################################################
if __name__ == '__main__':
	start=time.perf_counter()
	logging.info(f'测试开始, 总计账户 {len(accountPool[env])} 个')
	###################################################################
	def start_fuc(a,b):
		for acc in accountPool[env][a:b]:
			try:
				queryAccountAndHold(acc,'aaaa1111')
			except:
				logging.error(f'{acc} 发生异常:',exc_info=True)

	def getSplit(data_len,ths):
		t=int(data_len/ths)
		splits=[i*t for i in range(ths+1)]
		splits[-1]=data_len
		return splits
	###################################################################
	import threading
	threads=[];thread_num=1
	splits=getSplit(len(accountPool[env]),thread_num)
	for i in range(thread_num):
		t=threading.Thread(target=start_fuc,args=(splits[i],splits[i+1]))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
	###################################################################
	t=time.strftime('%H{h}%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(h='时',m='分',s='秒')
	logging.info(f'测试结束 耗时: {t}\n\n\n')

