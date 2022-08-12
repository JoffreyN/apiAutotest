import requests,logging,time,re,base64,sys,simplejson
from config import bossInfo

def __saveCookie(cookie,fileName):
	sys.path.append('..')
	with open(f'testData/{fileName}','w',encoding='utf-8') as f:
		f.write(cookie)

def getConfig(env):
	global host,head,uname,pwd
	host=bossInfo[env]['host']
	uname=bossInfo[env]['uname']
	pwd=bossInfo[env]['pwd']
	head={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
		'Cookie':'',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection':'close',
		'X-Requested-With':'XMLHttpRequest'
	}

def loginBoss(env):
	global host,head,uname,pwd
	url=f'{host}/admin/adminUser/login'
	for i in range(10):
		keys={
			"account":uname,
			"password":pwd,
			"vcode":"",
		}
		# head['Cookie'],keys['vcode']=getVcode(head)
		resp=requests.post(url,headers=head,data=keys)
		try:
			respJson=resp.json()
		except json.decoder.JSONDecodeError:
			logging.error(f'自动登录boss系统失败，登录接口返回异常: {resp.text}')
			continue
		if respJson['result']=='1':
			try:
				head['Cookie']=resp.headers['set-cookie']
			except KeyError:
				if i==9:raise KeyError
				head['Cookie']='0'
				continue
			__saveCookie(head['Cookie'],f'boss_{env}')
			return head['Cookie']
		else:
			logging.error(f'自动登录boss系统失败: {respJson}')
			logging.info(f'2秒后开始第 {i+1} 次重试...')
			time.sleep(2);head['Cookie']=''
	raise Exception(f'自动登录{env} boss系统失败')

def getBossCookie(env):
	logging.info('自动获取boss后台cookie')
	global head,host
	getConfig(env.lower())
	url=f'{host}/cms/cmsClient/list?type=1'
	try:
		cookieLogined=open(f'testData/boss_{env}').read().strip()
		logging.info('使用本地cookie')
	except FileNotFoundError:
		cookieLogined='0'
	for i in range(5):
		head['Cookie']=cookieLogined
		resp=requests.get(url,headers=head)
		if "/admin/AdminUser/" in resp.text:
			logging.info('boss后台cookie失效，重新登录…')
			cookieLogined=loginBoss(env)
			continue
		elif '高级搜索' in resp.text:
			return cookieLogined
		else:
			logging.info(f'登录boss失败: {resp.text}')
			sys.exit()
	raise Exception(f'获取 {env}环境 boss系统cookie失败')

######################################################################################################
# def quoteSwitch(types,env):
# 	global head,host
# 	getConfig(env.lower())
# 	url=f'{host}/admin/systemSwitch/changeActive'
# 	try:
# 		cookieLogined=open(f'testData/boss_{env}').read().strip()
# 	except FileNotFoundError:
# 		cookieLogined='0'
# 	if types=='jieli':# 启用捷力 关闭聚源
# 		key1={'msg':'启用捷力','data':{'id':'15','active':'true','code':'TELE_SOURCE'}}
# 		key2={'msg':'关闭聚源','data':{'id':'14','active':'false','code':'JY_SOURCE'}}
# 	elif types=='juyuan':# 启用聚源 关闭捷力
# 		key1={'msg':'关闭捷力','data':{'id':'15','active':'false','code':'TELE_SOURCE'}}
# 		key2={'msg':'启用聚源','data':{'id':'14','active':'true','code':'JY_SOURCE'}}
# 	for key in [key1,key2]:
# 		for i in range(5):
# 			head['Cookie']=cookieLogined
# 			resp=requests.post(url,headers=head,data=key['data'])
# 			respJson=resp.json()
# 			if respJson['result']=='302':
# 				logging.info('boss后台cookie失效，重新登录…')
# 				cookieLogined=loginBoss(env)
# 				continue
# 			elif respJson['result']=='1':
# 				print(f"{key['msg']} {respJson['data']}")
# 				# logging.info(f"{key['msg']} {respJson['data']}")
# 				break

if __name__ == '__main__':
	# quoteSwitch('jieli','dev')
	getBossCookie('test')