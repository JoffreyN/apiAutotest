# pip3 install requests HTMLReport websocket websocket-client numpy simplejson openpyxl pymysql jsonpath protobuf requests_toolbelt 
wsHost={
	'dev':'ws://0.0.0.0/ws',
	'test':'ws://0.0.0.0/ws',
	'uat':'ws://0.0.0.0/ws',
	'prod':'wss://0.0.0.0/ws'
}

domainJY={
	'dev':'http://0.0.0.0',
	'test':'http://0.0.0.0',
	'uat':'http://0.0.0.0',
	'prod':'https://0.0.0.0'
}

domainJL={
	'dev':'http://0.0.0.0',
	'test':'http://0.0.0.0',
	# 'uat':'https://0.0.0.0',
	'uat':'http://0.0.0.0',
}

domainCMBI={
	'dev':'http://0.0.0.0',
	'test':'http://0.0.0.0',
	'uat':'http://0.0.0.0',
	'prod':'https://0.0.0.0',
}

bossInfo={
	'uat':{
		'host':'http://0.0.0.0',
		'uname':'uatAdmin',
		'pwd':'Cmbi6688',
	},
	'prod':{
		'host':'https://0.0.0.0',
		'uname':'zhangteng',
		'pwd':'zhangteng123',
	},
	'test':{
		'host':'http://0.0.0.0',
		'uname':'uatAdmin',
		'pwd':'Cmbi6688',
	},
	'dev':{
		'host':'http://0.0.0.0',
		'uname':'uatAdmin',
		'pwd':'Cmbi6688',
	},
}

dataBaseInfo={
	'dev':{
		'host':'0.0.0.0',
		'uname':'****',
		'pword':'****',
		'dbName':'dev_quote_sync',
	},
	'test':{
		'host':'0.0.0.0',
		'uname':'****',
		'pword':'*******',
		'dbName':'test_quote_sync',
	},
	'uat':{
		'host':'0.0.0.0',
		'uname':'****',
		'pword':'*******',
		'dbName':'uat_quote_sync',
	},
}

accountPool={
	'uat':{'511703':'******','511682':'******'},
	'test':{'511703':'******','511682':'******'},
	'prod':{'568608':'******'},
}

marketCodeDic={161:'E',101:'B',105:'A',303:'N',302:'N'}
marketCodeNameDic={161:'HK',101:'SH',105:'SZ',303:'US'}
INIT_CONNECT=1001
KEEP_ALIVE=1004
QT_COMMAND_SUB=3001
QT_GetBasicQot=3004
QT_COMMAND_GetSnapshotQot=3005
QT_COMMAND_GetTimeShare=3008
QT_COMMAND_GetOrderBook=3012
QT_DATA_UpdateOrderBook=3303
QT_DATA_UpdateBasicQot=3302
QT_DATA_UpdateSnapshotQot=3301

# public static final short INIT_CONNECT = 1001;
# public static final short KEEP_ALIVE = 1004;
# public static final short QT_COMMAND_SUB = 3001;
# public static final short QT_COMMAND_GetSnapshotQot = 3005; // 请求行情快照
# public static final short QT_COMMAND_GetTimeShare = 3008; // 请求分时
# public static final short QT_COMMAND_GetOrderBook = 3012; //请求买卖档
# public static final short QT_DATA_UpdateOrderBook = 3303; //推送买卖档
# public static final short QT_DATA_UpdateBasicQot = 3302; // 推送简版行情快照
# public static final short QT_DATA_UpdateSnapshotQot = 3301; // 推送行情快照

receiver=['0.0.0.0.hk']
# receiver=['CMBI-0.0.0.0.hk']
mailToCc=['0.0.0.0','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk']
# mailToCc=['0.0.0.0.hk']
# receiver=['0.0.0.0.hk','CMBI-0.0.0.0.hk','0.0.0.0','0.0.0.0.hk','0.0.0.0']
# mailToCc=['0.0.0.0','0.0.0.0','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk','0.0.0.0.hk']#抄送

import sys,os
platform=sys.platform
genPath=os.path.join(sys.path[0],'report/')
if platform=='darwin':
	ip=[a for a in os.popen('ifconfig en2').readlines() if 'inet' in a][1].split()[1]
	port='80'
	host=f'http://{ip}:{port}/report'
	webPath='~/www/report/'
elif platform=='win32':
	ip=[a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
	port='80'
	host=f'http://{ip}:{port}/report'
	webPath='~/WWW/report'
elif platform=='linux':
	ip=''
	port=''
	host='report'
	webPath=''

# 个股快照 3301
# 简版行情 
# 分时 3008

from unittest import TestCase
assertObj=TestCase()


# pip3 install websocket-client numpy simplejson protobuf 