import time,traceback,logging
from config import dataBaseInfo

def getDBconn(host,user,password,dbType):
	if dbType=='mysql':
		import pymysql
		conn=pymysql.connect(host=host,user=user,password=password,charset='utf8')
	elif dbType=='postgresql':
		import psycopg2
		conn=psycopg2.connect(host=host,user=user,password=password,port="30003",database="omsfund")

	# elif dbType=='sqlserver':
	# 	user='api';password='Abcd1234'
	# 	hostDic={'uat':'0.0.0.0','test':'0.0.0.0'}
	# 	import pymssql
	# 	conn=pymssql.connect(server=hostDic[env],user=user,password=password)
	# conn.ping(reconnect=True)
	return conn

def excuteSQL(conn,sql,logit=1):
	cursor=conn.cursor()
	results=0
	try:
		if type(sql)==list:
			for s in sql:
				cursor.execute(s)
				if logit:print(f'执行成功: {s}')
			results=1
		else:
			cursor.execute(sql)
			if logit:print(f'执行成功: {sql}')
			results=cursor.fetchall() if sql.startswith('SELECT') else 1
		cursor.close()
		conn.commit()
	except Exception as e:
		conn.rollback() # 事务回滚
		logging.info(f'SQL执行失败 {[sql]}\n{traceback.format_exc()}')
	finally:
		conn.close()
	return results
	
def queryCodelist(marketCode,lens=10,sql=None,env='test',idLimit=None):
	# id 34079~37491 港股正股
	# id 37492~44187 港股认购证
	# id 44188~44523 不知道
	# id 44523~45360 港股 界
	# id 45361~53921 港股牛熊证
	# id 53922~53963 港股 R
	# id 53964~54005 港股 不知道
	# id 54006~54039 港股国债
	conn=getDBconn(dataBaseInfo[env]['host'],dataBaseInfo[env]['uname'],dataBaseInfo[env]['pword'],'mysql')
	if not sql:
		if idLimit:
			sql=f"SELECT stock_code,stock_name FROM {dataBaseInfo[env]['dbName']}.t_stock_info WHERE market_code='{marketCode}' and enable_search=1 and status='VALID' and id>={idLimit[0]} and id<={idLimit[1]} order by rand() limit {lens};"
		else:
			sql=f"SELECT stock_code,stock_name FROM {dataBaseInfo[env]['dbName']}.t_stock_info WHERE market_code='{marketCode}' and enable_search=1 and status='VALID' order by rand() limit {lens};"
	return excuteSQL(conn,sql)

def getOmsFundData():
	conn=getDBconn('0.0.0.0','postgres','****','****')
	sql='SELECT * FROM omsfund.public.holiday'
	return excuteSQL(conn,sql)

def getInnerCompanyCode(stockCode):
	conn=getDBconn('0.0.0.0','****','****','mysql')
	sql=f"SELECT SECURITYCODE,SECINNERCODE,COMPANYCODE FROM dcmg.CDSY_SECUCODE WHERE SECURITYCODE ='{stockCode}';"
	result=excuteSQL(conn,sql,0)
	return result[0] if result else (stockCode,None,None)



