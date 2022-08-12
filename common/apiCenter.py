import requests,time,logging
from jsonpath import jsonpath

def login_ttl(uname,pword,env='test'):
	head={
		'User-Agent':'zyapp/2.2.1.36591 (HONOR COLAL10; Android 9) uuid/VBJDU19510007442 channel/Atest1 redgreensetting/red language/zhCN versionCode/33562625',
		'Content-Type':'application/json;charset=UTF-8',
		'Connection':'close',
	}
	url=f'http://trade-{env}.****.***/auth-center/public/login/accountLogin'
	data={"traceLogId":f"fromzp_{time.time()}","accountNo":uname,"tradePwd":pword}
	resp=requests.post(url,headers=head,json=data)
	respJson=resp.json()
	# print(f'{uname} debug: {respJson}')
	if respJson['success']:
		sessionDic={
			'token':jsonpath(respJson,'$..loginToken')[0],
			'sessionId':jsonpath(respJson,'$..session')[0],
			'acctType':'MRGN' if 'M' in uname else 'CASH',
			'aeCode':jsonpath(respJson,'$..aeCode')[0],
			'marginMax':jsonpath(respJson,'$..marginMax')[0],
			'accountId':uname,
			'accountName':jsonpath(respJson,'$..acctName')[0],
			'operatorNo':jsonpath(respJson,'$..operatorNo')[0],
		}
		return sessionDic
	else:
		raise Exception(f'{uname}登录失败: {respJson}')

if __name__ == '__main__':
	pass
