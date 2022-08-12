import time,logging,traceback,unittest,requests,json,sys
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase
from common.tools import readExcel
from common.apiCenter import login_ttl

from jsonpath import jsonpath
from urllib3 import encode_multipart_formdata

# @unittest.skip('跳过')
@ddt.ddt
class TestAuto(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 接口测试开始 ########## ')
		cls.head={'Connection':'close'}
		cls.sessionDic=login_ttl(cls.args.account,'aaaa1111',cls.args.env)
		# cls.m_sessionDic=login_ttl(f"M{cls.args.account}",'aaaa1111',cls.args.env)

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	@no_retry
	@ddt.data(*readExcel(globals()['sys'].argv))
	def test_Auto(self,lineDic):
		logging.info(f' ========== {lineDic["desc"]} 测试开始 ========== ')
		null=None;true=True;false=False
		traceLogId=f'fromZP_{time.time()}'
		token=self.__class__.sessionDic['token']
		sessionId=self.__class__.sessionDic['sessionId']
		acctType=self.__class__.sessionDic['acctType']
		aeCode=self.__class__.sessionDic['aeCode']
		marginMax=self.__class__.sessionDic['marginMax']
		accountId=self.__class__.sessionDic['accountId']
		accountName=self.__class__.sessionDic['accountName']
		operatorNo=self.__class__.sessionDic['operatorNo']

		
		# m_token=self.__class__.m_sessionDic['token']
		# m_sessionId=self.__class__.m_sessionDic['sessionId']
		# m_acctType=self.__class__.m_sessionDic['acctType']
		# m_aeCode=self.__class__.m_sessionDic['aeCode']
		# m_marginMax=self.__class__.m_sessionDic['marginMax']
		m_accountId=f"M{self.args.account}"
		# m_accountName=self.__class__.m_sessionDic['accountName']
		# m_operatorNo=self.__class__.m_sessionDic['operatorNo']

		if lineDic["skip"]!='No':self.skipTest("跳过")
		if lineDic["type"].lower()=='dubbo':self.skipTest("暂不支持dubbo接口测试")
		proxy=eval(lineDic["proxy"]) if lineDic["proxy"] else None
		url=f'{lineDic["type"].lower()}://{lineDic["host"]}{lineDic["reqPath"]}'
		logging.info(f'请求URL: {url}')
		if lineDic["dataType"]=='json':
			self.__class__.head["Content-Type"]="application/json;charset=UTF-8"
			reqData=eval(lineDic["reqData"])
			# data=None
			logging.info(f'请求Jsondata: {reqData}')
		elif lineDic["dataType"]=='urlencode':
			self.__class__.head["Content-Type"]="application/x-www-form-urlencoded;charset=UTF-8"
			# jsonData=None
			try:
				reqData=eval(lineDic["reqData"])
			except:
				reqData=lineDic["reqData"]
			logging.info(f'请求data: {reqData}')
		elif lineDic["dataType"]=='file':
			# jsonData=None
			self.assertTrue(os.path.exists(lineDic["reqData"]),f'文件 {lineDic["reqData"]} 不存在！')
			logging.info(f'请求文件: {lineDic["reqData"]}')
			encode_data=encode_multipart_formdata({'file':(os.path.split(lineDic["dataType"])[1],open(lineDic["dataType"],'rb').read())})
			reqData=encode_data[0]
			self.__class__.head['Content-Type']=encode_data[1]
		if lineDic["reqHeader"]:self.__class__.head.update(eval(lineDic["reqHeader"]))

		_start=time.perf_counter()
		if lineDic["reqType"]=='GET':
			resp=requests.get(url,headers=self.__class__.head,params=reqData,verify=False,proxies=proxy)
		elif lineDic["reqType"]=='POST':
			if lineDic["dataType"]=='urlencode':
				resp=requests.post(url,headers=self.__class__.head,data=reqData,verify=False,proxies=proxy)
			elif lineDic["dataType"]=='json':
				resp=requests.post(url,headers=self.__class__.head,json=reqData,verify=False,proxies=proxy)
		else:
			self.skipTest(f'暂不支持的方法: {lineDic["reqType"]}')
		_spendTime=f"{int((time.perf_counter()-_start)*1000)} ms"

		status=resp.status_code
		self.assertTrue(status,f'状态码: {status}')
		if lineDic["checkType"]=='text':
			checkData=respData=resp.text
		else:
			respData=resp.json()
			try:
				checkData=jsonpath(respData,lineDic["checkType"])[0]
			except TypeError:
				checkData=None
		logging.info(f'返回数据: {respData}')
		logging.info(f'耗时: {_spendTime}')

		if lineDic["checkMode"]=='相等':
			self.assertEqual(lineDic["checkPoint"],str(checkData))
		elif lineDic["checkMode"]=='包含':
			self.assertIn(lineDic["checkPoint"],str(checkData))

		logging.info(f' ========== {lineDic["desc"]} 测试结束 ========== ')


	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()