import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from common.parameter import ParameTestCase

from common.tools import postReq,jsonpath_getOne
from common.database import getOmsFundData
# 基金日历数据对比

fundList=[("IE0000931182","USD"),("LU0260870406","EUR"),("HK0000039831","USD"),("HK0000039989","HKD"),]

# @unittest.skip('跳过')
@ddt.ddt
class TestFundCompare(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 基金日历数据对比 接口测试开始 ########## ')

	def setUp(self):
		pass

	# @ddt.data(*fundList)
	@no_retry
	def test_01(self):
		logging.info(f' ========== 测试开始 ========== ')
		# omsFundData=getOmsFundData()
		omsFundData=[(0,0,"LU1171460220","USD"),]
		# omsFundData=[(0,0,"LU1171460220","USD"),(0,0,"LU0516397667","USD"),(0,0,"LU1342487771","USD"),(0,0,"LU0149524976","HKD"),(0,0,"HK0000554177","USD"),]

		logging.info(f'查询到数据库中基金日历数据共 {len(omsFundData)} 条')
		url="http://0.0.0.0/pbop-fund-service/rest/1.0/subscription/mf/product-keys/action/batch-push?accessKey=cmbi&expires=1609746893328&timestamp=1609746888328&sign=v2svMH4wFla/QYI1Jv2CXlLkf8Xk+MNOI4tEtbxQ78QEiku/cleogj7ZPNgpLpvUlAjfR/SI/q1gOtc0+w0pSA=="
		dataJson={
			"data":
			{
				"subscriber": "201701",
				"systemCode": "CMBI",
				"dataSource": "ALLFUNDS",
				"instrKeyList": [{"idType": "ISIN","identifier":"","currency":""}]
			},
			"traceLogId":f"FromZP{str(time.time()).replace('.','')}"
		}
		failed=0
		for item in omsFundData:
			dataJson['data']['instrKeyList'][0]['identifier']=item[2]
			dataJson['data']['instrKeyList'][0]['currency']=item[3]
			logging.info(f'请求数据: {dataJson}')
			respJson=postReq(0,dataJson,0,url=url,mod='post',nolog=1)
			logging.info(f'返回数据: {respJson}')
			logging.info(f'对应的数据库中数据: {item}')
			n=0
			for i in item[5:]:
				n+=1
				dayMonthData=jsonpath_getOne(respJson,f'dayMonth{n}','str')
				if i!=dayMonthData:
					failed+=1
					logging.info(f'{item[2]} 第 {n} 月数据对比失败: {dayMonthData} != {i}')
				else:
					logging.info(f'{item[2]} 第 {n} 月数据对比成功')
			logging.info(f'\n')
		self.assertEqual(0,failed)
		logging.info(f' ========== 测试结束 ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 基金日历数据对比 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()