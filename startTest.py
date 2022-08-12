# -*- coding: utf-8 -*-
import HTMLReport,time,os,logging,argparse,traceback
from websocket import create_connection

from testSuite.suite import loadSuite
from common.tools import moveFiles,sendMail
from client import *
from config import *

def getParser():
	parser=argparse.ArgumentParser(description='接口测试',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="指定运行环境(默认 test)：\n\tUAT\tUAT环境\n\tTEST\tTEST环境\n\tDEV\tDEV环境\n\tPROD\t生产环境",required=False,default='test')
	parser.add_argument('-a',dest='account',help="指定账号(默认 511703)",required=False,default='511703')
	parser.add_argument('-s',dest='suite',help="指定需要执行的用例集(默认 quote):\n\tall\t\t所有用例集\n\tquote\t\tquote-query接口用例集\n\tnode\t\tnode网关接口用例集\n\twebsocket\twebsocket接口用例集\n\tF10_US\t\t美股F10相关接口\n\tF10_HK\t\t港股F10相关接口\n\tF10_A\t\tA股F10相关接口\n\tjl_update\t捷力升级数据对比\n\tfundcompare\t基金日历数据对比\n\tnewMarket\t新版市场行情\n\tanpan\t\t暗盘测试\n\tpublic\t\t大众版行情测试\n\tcurrExchange\tboss端货币兑换\n\tauto\t\t根据Excel自动开始测试",required=False,default='quote')
	parser.add_argument('--compare',help="与指定的第三方数据进行对比(默认不对比):\n\tjl\t捷力数据\n\tgf\t广发数据\n\tft\t富途数据",required=False,default=None)
	parser.add_argument('--excelName',help="当要测试的用例集包含auto时，必须指定Excel名称",required=False,default=None)
	parser.add_argument('--skipWarrants',help="跳过涡轮代码",action='store_true',required=False)
	parser.add_argument('-t',dest='thead',help="指定并发线程数(默认 20)",type=int,required=False,default=20)
	parser.add_argument("--getTokenFromRedis",help=argparse.SUPPRESS,action='store_true',required=False)
	parser.add_argument('--sendMail',help="自动发送邮件",action='store_true',required=False)
	parser.add_argument("--receiver",help=argparse.SUPPRESS,required=False)
	parser.add_argument("--fromInfo",help=argparse.SUPPRESS,required=False)
	args=parser.parse_args()
	return args

def main():
	args.env=args.env.lower()
	args.qotToken=None
	wsConn=create_connection(wsHost[args.env])
	now=time.strftime('%Y%m%d%H%M%S')
	args.timeStr=f"api_{args.env}_{now}"
	suites=loadSuite(wsConn,args)
	reportURL=f'{host}/{args.timeStr}'
	desc=f'被测ws地址：<span class="info">{wsHost[args.env]}</span>' if 'websocket' in args.suite else ''
	result=HTMLReport.TestRunner(
		title="接口测试报告",
		description=desc,
		output_path=f'report/{args.timeStr}',
		report_file_name='index',
		sequential_execution=True,#按照套件添加(addTests)顺序执行
		tries=2,
		thread_count=args.thead,
		delay=1,
		retry=True,
	).run(suites)
	wsConn.close()
	try:moveFiles(args.timeStr,'copy')
	except:print(traceback.format_exc())

	print('报告链接：',reportURL)
	# if platform=='darwin':
	# 	os.system(f'open {reportURL}')
	# elif platform=='win32':
	# 	os.system(f'start {reportURL}')
	# else:
	# 	print('platform:',platform)

	if args.sendMail:
		if result.failure_count+result.error_count or args.suite=='currExchange':
			foot=f'<p>网页版请<a href="{reportURL}">点击这里</a>查看(提示：请用 CMBI 网络访问)</p><br/>'
			text=open(os.path.expanduser(os.path.join(webPath,args.timeStr,'index.html')),'r',encoding='utf-8').read()
			sendMail(text=f'{foot}{text}',platformName=args.env.upper(),fromInfo=args.fromInfo,cusReceiver=args.receiver)
	# return reportURL,args.timeStr
	return result

if __name__=='__main__':
	args=getParser()
	if args.suite=='all' or 'auto' in args.suite:
		if args.excelName:
			if args.excelName.endswith('.xlsx'):pass
			else:raise Exception(f'输入的Excel文件名称错误: {args.excelName}')
		else:
			raise Exception(f'未指定Excel文件名称')
	result=main()
	try:
		resultList=open(f'result_{args.timeStr}.txt','r',encoding='utf-8').readlines()
		resultList.sort(key=lambda x:float(x.split()[-1]),reverse=True)
		with open(f'result_{args.timeStr}.txt','w',encoding='utf-8') as file:file.writelines(resultList)
	except FileNotFoundError:
		pass
	os.environ.setdefault('ALL_PASS','True')
	os.environ["ALL_PASS"]=str(result.failure_count+result.error_count)
	sys.exit(result.failure_count+result.error_count)

