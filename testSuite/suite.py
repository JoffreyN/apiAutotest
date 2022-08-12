import unittest
from common.parameter import ParameTestCase

from testCase.testQuotation import TestQuotation
from testCase.testWebsocket import TestWebsocket
from testCase.testNode import TestNode
from testCase.testF10_US import TestF10_US
from testCase.testF10_HK import TestF10_HK
from testCase.testF10_A import TestF10_A
from testCase.testJieliUpdate import TestJLupdate
from testCase.testFundcompare import TestFundCompare
from testCase.testNewMarket import TestNewMarket
from testCase.testAnpan import TestAnpan
from testCase.testPublicQuote import TestPublicQuote
from testCase.testBossCurrExchange import TestBossCurrExchange
from testCase.testAuto import TestAuto

def loadSuite(wsConn,args):
	testCasesDic={
		'quote':TestQuotation,
		'node':TestNode,
		'websocket':TestWebsocket,
		'F10_US':TestF10_US,
		'F10_HK':TestF10_HK,
		'F10_A':TestF10_A,
		'jl_update':TestJLupdate,
		'fundcompare':TestFundCompare,
		'newMarket':TestNewMarket,
		'anpan':TestAnpan,
		'auto':TestAuto,
		'public':TestPublicQuote,
		'currExchange':TestBossCurrExchange,
	}
	testSuite=unittest.TestSuite()
	for sName in args.suite.split():
		if sName=='all':
			for suiteName,testClass in testCasesDic.items():
				__testClass=testCasesDic[sName]
				__testClass.args=args
				testSuite.addTest(ParameTestCase.paramed(__testClass,wsConn=wsConn,args=args))
		else:
			try:
				__testClass=testCasesDic[sName]
				__testClass.args=args
				testSuite.addTest(ParameTestCase.paramed(__testClass,wsConn=wsConn,args=args))
			except KeyError:
				raise Exception(f'未知的测试用例集: {sName}')
	return testSuite