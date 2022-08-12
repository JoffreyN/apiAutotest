import json,time
from common.tools import jsonpath_getOne,saveTodatabase,formatSqlStr
from common import pbjson
from client import parseData

def parse_ws_json(jsonPath,app_version):
	pcapJson=json.loads(open(jsonPath,'r',encoding='utf-8').read())
	sqlList=[]
	for item in pcapJson:
		try:
			datadata=jsonpath_getOne(item,'data')['data.data'].replace(':','')
		except TypeError:
			pass
			# print('Error:',item)
		code,resp=parseData(bytes.fromhex(datadata),'request')
		# code,resp=parseData(bytes.fromhex(jsonpath_getOne(item,'data')['data.data'].replace(':','')),'request')
		dataJson=json.loads(pbjson.pb2json(resp))
		print(f"websocket请求: {code} {dataJson}")
		created_at=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(jsonpath_getOne(item,'frame')['frame.time_epoch'])))
		try:
			if code==1001:
				if dataJson['c2s']['deviceType']==1:
					device_type='Android'
				elif dataJson['c2s']['deviceType']==0:
					device_type='iOS'
		except KeyError:
			device_type='未知设备'
		sqlList.append(f"INSERT INTO interfaceTest_data.count_websocket (created_at,device_type,app_version,req_code,req_data) VALUES ('{created_at}','{device_type}','{app_version}','{code}','{formatSqlStr(dataJson)}');")
	saveTodatabase(sqlList)

if __name__ == '__main__':
	jsonPath=input('输入json文件路径: ')
	app_version=input('输入APP版本: ')
	parse_ws_json(jsonPath,app_version)