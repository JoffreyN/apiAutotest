import time,logging,unittest,requests,simplejson,copy,sys
from requests_toolbelt import MultipartEncoder
from HTMLReport import ddt,no_retry
from random import uniform

from bs4 import BeautifulSoup
from common.parameter import ParameTestCase
from common.boss import getBossCookie
from config import bossInfo
from testData.data import currExchange_Data

# @unittest.skip('跳过')
@ddt.ddt
class TestBossCurrExchange(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## boss货币兑换 接口测试开始 ########## ')
		cls.bossCookie=getBossCookie(cls.args.env)
		cls.head={
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			'Cookie':cls.bossCookie,
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Connection':'close',
			'X-Requested-With':'XMLHttpRequest'
		}

	def setUp(self):
		pass

	def get_homeList(self):
		url=f'{bossInfo[self.args.env]["host"]}/frame/body/load?link_id=182'
		resp=requests.get(url,headers=self.__class__.head,verify=False)
		soup=BeautifulSoup(resp.text,'lxml')
		currUrl=soup.select_one('iframe')['src']

		resp=requests.get(currUrl,headers=self.__class__.head,verify=False)
		# print(resp.text)
		# sys.exit()
		respJson=self.checkJson(url,resp)
		logging.info(f'{url} 返回数据: {respJson}')
		logging.info(f"永隆港元今日兑出: {respJson['data']['tradeData']['WING_LUNG']['HKD']['amountCount']}")
		logging.info(f"永隆港元账户余额: {respJson['data']['tradeData']['WING_LUNG']['HKD']['avlBalance']}")
		logging.info(f"永隆港元OD余额: {respJson['data']['tradeData']['WING_LUNG']['HKD']['overdraft']}")
		logging.info(f"永隆美元今日兑出: {respJson['data']['tradeData']['WING_LUNG']['USD']['amountCount']}")
		logging.info(f"永隆美元账户余额: {respJson['data']['tradeData']['WING_LUNG']['USD']['avlBalance']}")
		logging.info(f"永隆美元OD余额: {respJson['data']['tradeData']['WING_LUNG']['HKD']['overdraft']}")
		logging.info(f"永隆人民币今日兑出: {respJson['data']['tradeData']['WING_LUNG']['CNY']['amountCount']}")
		logging.info(f"永隆人民币账户余额: {respJson['data']['tradeData']['WING_LUNG']['CNY']['avlBalance']}")
		logging.info(f"永隆人民币OD余额: {respJson['data']['tradeData']['WING_LUNG']['HKD']['overdraft']}")

		logging.info(f"渣打港元今日兑出: {respJson['data']['tradeData']['SCB']['HKD']['amountCount']}")
		logging.info(f"渣打港元账户余额: {respJson['data']['tradeData']['SCB']['HKD']['avlBalance']}")
		logging.info(f"渣打港元OD余额: {respJson['data']['tradeData']['SCB']['HKD']['overdraft']}")
		logging.info(f"渣打美元今日兑出: {respJson['data']['tradeData']['SCB']['USD']['amountCount']}")
		logging.info(f"渣打美元账户余额: {respJson['data']['tradeData']['SCB']['USD']['avlBalance']}")
		logging.info(f"渣打美元OD余额: {respJson['data']['tradeData']['SCB']['HKD']['overdraft']}")
		logging.info(f"渣打人民币今日兑出: {respJson['data']['tradeData']['SCB']['CNY']['amountCount']}")
		logging.info(f"渣打人民币账户余额: {respJson['data']['tradeData']['SCB']['CNY']['avlBalance']}")
		logging.info(f"渣打人民币OD余额: {respJson['data']['tradeData']['SCB']['HKD']['overdraft']}")
		
	def get_accountinfo(self):
		url=f'http://{self.args.env}-boss-combine.cmbi.online/admin/currencyExchange/accountinfo?accountId={self.args.account}'
		resp=requests.get(url,headers=self.__class__.head,verify=False)
		respJson=self.checkJson(url,resp)
		logging.info(f'{url} 返回数据: {respJson}')
		accName=respJson['data']['name']
		aeCode=respJson['data']['aecode']
		return accName,aeCode

	def get_rate(self,side,cur_in,cur_out,amount):
		channelDic={'WING_LUNG':'永隆','SCB':'渣打'}
		url=f'http://{self.args.env}-boss-combine.cmbi.online/admin/currencyExchange/getRate'
		data={
			'currencyIn':cur_in,
			'currencyOut':cur_out,
			'amount':amount,
			'side':side,
		}
		logging.info(f'{url} 请求数据: {data}')
		resp=requests.post(url,headers=self.__class__.head,data=data)
		respJson=self.checkJson(url,resp)
		logging.info(f'{url} 返回数据: {respJson}')
		rate=respJson['result']['rate']
		amountOut=respJson['result']['amountOut']
		exchangeChannel=respJson['result']['exchangeChannel']
		rateQuoteId=respJson['result']['rateQuoteId']
		logging.info(f'当前兑换线路: {channelDic[exchangeChannel]}银行')
		return rate,amountOut,exchangeChannel,rateQuoteId

	def save_currExchange(self,side,exchangeChannel,rateQuoteId,accName,aeCode,cur_in,cur_out,amountOut,amount,rate):
		url=f'http://{self.args.env}-0.0.0.0/admin/currencyExchange/save'
		sideDic={'in':'1','out':'2'}
		data={
			'serialNum':f"FromZP{time.time()}",
			'side':side,
			'exchangeChannel':exchangeChannel,
			'rateQuoteId':rateQuoteId,
			'isAllowClearingAcceptOrder':'',
			'accountId':self.args.account,
			'accountName':accName,
			'aeCode':aeCode,
			'currencyIn':cur_in,
			'currencyOut':cur_out,
			'amount':'',
			'amountOut':amountOut,
			'amountIn':amount,
			'rate':rate,
			'recordNo':'',
		}
		logging.info(f'{url} 请求数据: {data}')
		m=MultipartEncoder(fields=data)
		head=copy.deepcopy(self.__class__.head)
		head['Content-Type']=m.content_type

		resp=requests.post(url,headers=head,data=m)
		respJson=self.checkJson(url,resp)
		logging.info(f'{url} 返回数据: {respJson}')
		if respJson['result']=='CEX500204':
			data['isAllowClearingAcceptOrder']='1'
			m=MultipartEncoder(fields=data)
			head=copy.deepcopy(self.__class__.head)
			head['Content-Type']=m.content_type
			resp=requests.post(url,headers=head,data=m)
			respJson=self.checkJson(url,resp)
			logging.info(f'{url} 返回数据: {respJson}')
		return respJson

	def checkJson(self,url,resp):
		try:
			respJson=resp.json()
			return respJson
		except (simplejson.errors.JSONDecodeError,IndexError):
			logging.info(f'{url} 返回数据异常：{resp.text}')
			raise Exception('解析返回json失败')

	# @unittest.skip('跳过')
	# @no_retry
	@ddt.data(*currExchange_Data)
	@ddt.unpack
	def test_bossCurrExchange(self,in_out,cur_in,cur_out):
		'''货币兑换测试'''
		# if self.args.env=='uat':
		# 	if not (cur_in=='USD' and cur_out=='HKD'):self.skipTest('跳过')
		in_out_Dic={'in':'买入金额','out':'卖出金额'}
		sideDic={'in':'1','out':'2'}
		amount=str(round(uniform(100,1000),2))
		logging.info(f' ========== 测试开始 boss货币兑换 {in_out_Dic[in_out]} {cur_in}-->{cur_out} ========== ')
		self.get_homeList()
		logging.info('')
		accName,aeCode=self.get_accountinfo()
		logging.info('')
		rate,amountOut,exchangeChannel,rateQuoteId=self.get_rate(sideDic[in_out],cur_in,cur_out,amount)
		logging.info('')
		respJson=self.save_currExchange(sideDic[in_out],exchangeChannel,rateQuoteId,accName,aeCode,cur_in,cur_out,amountOut,amount,rate)
		self.assertEqual('1',respJson['result'])

		logging.info(f' ========== 测试结束 boss货币兑换 {in_out_Dic[in_out]} {cur_in}-->{cur_out} ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(self):
		logging.info(' ########## boss货币兑换 接口测试结束 ########## ')

if __name__=='__main__':
	unittest.main()