# 所有港股名单 包含衍生品
# curl -l -H "Content-type: application/json" -X POST -d '{"Ver": 1, "markets": [{"exchange": 161}]}' http://0.0.0.0:9080/v1/codelist
# type2
# ST_DW_CALL = 1402; // 认购衍生权证
# ST_DW_PUT = 1403; // 认估衍生权证
# ST_CBBC_BULL = 2001; // 牛证
# ST_CBBC_BEAR = 2002; // 熊证

# 101 上交所
# 105 深交所
# 161 港股
# 303 纽交所
# 302 纳斯达克

# A=深圳  B=上海   E=HK  N=美
# scene=0 简洁版数据
# scene=1 全部数据


# curl -l -H "Content-type: application/json" -X POST -d '{"id": {"exchange": 161, "code": "HSI"}, "scene": 0, "subscribe": false}' http://0.0.0.0:9080/v1/realtime
# curl -l -H "Content-type: application/json" -X POST -d '{"id": {"exchange": 161, "code": "HSI"}, "scene": 0, "subscribe": false}' http://0.0.0.0:9080/v1/realtime


# suspended 和 active同为NO为退市
# suspended YES&active YES 暂时停牌 
# suspended YES&active NO 可以过滤
# 🉑
codeData=[]
# codeData=[
# 	# {'types':'HK','code':'00700','name':'腾讯控股','mkCode':161},# type2=1003
# 	# {'types':'HKN','code':code,'name':name,'mkCode':161},#牛证 type2=2001
# 	# {'types':'HKX','code':code,'name':name,'mkCode':161},#熊证 type2=2002
# 	# {'types':'HKZ','code':code,'name':name,'mkCode':161},#认购 type2=1402
# 	# {'types':'HKG','code':code,'name':name,'mkCode':161},#认沽 type2=1403
# 	# {'types':'US','code':code,'name':name,'mkCode':302},# 302 或 303
# 	# {'types':'SH','code':code,'name':name,'mkCode':101},# type2=1001
# 	# {'types':'SZ','code':code,'name':name,'mkCode':105},# type2=1001
# 	{'types':'zhishu','code':'HSI','name':'恒生指数','mkCode':161},
# 	{'types':'zhishu','code':'HSCEI','name':'国企指数','mkCode':161},
# 	{'types':'zhishu','code':'HSCCI','name':'红筹指数','mkCode':161},
# 	# {'types':'zhishu','code':'DJI','name':'道琼斯','mkCode':303},
# 	# {'types':'zhishu','code':'IXIC','name':'纳斯达克','mkCode':303},
# 	# {'types':'zhishu','code':'SPX','name':'标普500','mkCode':303},
# 	{'types':'zhishu','code':'399001','name':'深证成指','mkCode':105},
# 	{'types':'zhishu','code':'000001','name':'上证指数','mkCode':101},
# 	{'types':'zhishu','code':'399300','name':'沪深300','mkCode':105},
# ]

# 同花顺数据中心 http://0.0.0.0/hgt/sgtb/?_da0.6043541851370857
# 同花顺港股数据 http://0.0.0.0/hk/indexYs/
# 新浪数据 涡轮行情 http://0.0.0.0/hkstock/warrants/00388.html

# 中华通=沪港通（沪股通+港股通）+ 深港通（深股通+港股通）

# 161=E,101=B,105=A,303=N
codeData_active=[
	{'types':'zhishu','code':'HSI','name':'恒生指数','mkCode':161},
	{'types':'zhishu','code':'HSCEI','name':'国企指数','mkCode':161},
	{'types':'zhishu','code':'HSCCI','name':'红筹指数','mkCode':161},
	{'types':'zhishu','code':'DJI','name':'道琼斯','mkCode':303},
	{'types':'zhishu','code':'IXIC','name':'纳斯达克','mkCode':303},
	{'types':'zhishu','code':'SPX','name':'标普500','mkCode':303},
	{'types':'zhishu','code':'399001','name':'深证成指','mkCode':105},
	{'types':'zhishu','code':'000001','name':'上证指数','mkCode':101},
	{'types':'zhishu','code':'000300','name':'沪深300','mkCode':101},
	# 沪股通
	{'types':'SH','code':'600036','name':'招商银行','mkCode':101},
	{'types':'SH','code':'600519','name':'贵州茅台','mkCode':101},
	{'types':'SH','code':'600030','name':'中信证券','mkCode':101},
	{'types':'SH','code':'601628','name':'中国人寿','mkCode':101},
	{'types':'SH','code':'600196','name':'复星医药','mkCode':101},
	#深股通
	{'types':'SZ','code':'300750','name':'宁德时代','mkCode':105},
	{'types':'SZ','code':'000858','name':'五粮液','mkCode':105},
	{'types':'SZ','code':'000651','name':'格力电器','mkCode':105},
	{'types':'SZ','code':'002475','name':'立讯精密','mkCode':105},
	{'types':'SZ','code':'000901','name':'航天科技','mkCode':105},
	# # 沪港通
	{'types':'HK','code':'00700','name':'腾讯控股','mkCode':161},
	{'types':'HK','code':'00981','name':'中芯国际','mkCode':161},
	{'types':'HK','code':'01810','name':'小米集团-W','mkCode':161},
	{'types':'HK','code':'00728','name':'中国电信','mkCode':161},
	{'types':'HK','code':'03968','name':'招商银行','mkCode':161},
	# # 港股非沪港通
	{'types':'HK','code':'02888','name':'渣打集团','mkCode':161},
	{'types':'HK','code':'00005','name':'汇丰控股','mkCode':161},
	{'types':'HK','code':'00027','name':'银河娱乐','mkCode':161},
	{'types':'HK','code':'00001','name':'长和','mkCode':161},
	{'types':'HK','code':'02378','name':'保诚','mkCode':161},
	# # 创业板
	{'types':'SZ','code':'300033','name':'同花顺','mkCode':105},
	{'types':'SZ','code':'300773','name':'拉卡拉','mkCode':105},
	{'types':'SZ','code':'300783','name':'三只松鼠','mkCode':105},
	{'types':'SZ','code':'300748','name':'金力永磁','mkCode':105},
	{'types':'SZ','code':'300051','name':'三五互联','mkCode':105},
	{'types':'SZ','code':'300189','name':'神农基因','mkCode':105},
	{'types':'SZ','code':'300059','name':'东方财富','mkCode':105},
	{'types':'SZ','code':'300024','name':'机器人','mkCode':105},
	{'types':'SZ','code':'300015','name':'爱尔眼科','mkCode':105},
	{'types':'SZ','code':'300146','name':'汤臣倍健','mkCode':105},
	# # 港股创业板
	{'types':'HK','code':'08225','name':'中国医疗集团','mkCode':161},
	{'types':'HK','code':'08300','name':'皇玺餐饮集团','mkCode':161},
	{'types':'HK','code':'08328','name':'信义香港','mkCode':161},
	{'types':'HK','code':'08329','name':'海王英特龙','mkCode':161},
	{'types':'HK','code':'08162','name':'港银控股','mkCode':161},
	{'types':'HK','code':'08051','name':'讯智海','mkCode':161},
	{'types':'HK','code':'08153','name':'法诺集团','mkCode':161},
	{'types':'HK','code':'08083','name':'中国有赞','mkCode':161},
	{'types':'HK','code':'08163','name':'领智金融','mkCode':161},
	{'types':'HK','code':'08170','name':'全民国际','mkCode':161},
	# # AH股
	{'types':'HK','code':'01108','name':'洛阳玻璃股份','mkCode':161},
	{'types':'HK','code':'01349','name':'复旦张江','mkCode':161},
	{'types':'HK','code':'01456','name':'国联证券','mkCode':161},
	{'types':'HK','code':'00038','name':'第一拖拉机股份','mkCode':161},
	{'types':'HK','code':'00042','name':'东北电气','mkCode':161},
	{'types':'HK','code':'02880','name':'大连港','mkCode':161},
	{'types':'HK','code':'02318','name':'中国平安','mkCode':161},
	{'types':'HK','code':'00914','name':'海螺水泥','mkCode':161},
	{'types':'HK','code':'00939','name':'建设银行','mkCode':161},
	{'types':'HK','code':'02899','name':'紫金矿业','mkCode':161},
	# # 牛熊证
	# {'types':'HKN','code':'57486','name':'港交法兴零乙牛J','mkCode':161},#牛 type2=2001
	# {'types':'HKN','code':'57053','name':'港交摩通一一牛C','mkCode':161},#牛 type2=2001
	# {'types':'HKN','code':'60088','name':'港交瑞银零乙牛J','mkCode':161},#牛 type2=2001
	{'types':'HKN','code':'64282','name':'港交法巴一九牛G','mkCode':161},#牛 type2=2001
	# {'types':'HKN','code':'61774','name':'港交高盛一三牛B','mkCode':161},#牛 type2=2001
	# {'types':'HKX','code':'61714','name':'港交摩利一五熊A','mkCode':161},#熊 type2=2002
	# {'types':'HKX','code':'64985','name':'港交法兴一五熊A','mkCode':161},#熊 type2=2002
	# {'types':'HKX','code':'63876','name':'港交瑞通一六熊E','mkCode':161},#熊 type2=2002
	# {'types':'HKX','code':'58961','name':'港交瑞通一六熊D','mkCode':161},#熊 type2=2002
	# {'types':'HKX','code':'68917','name':'港交法兴一二熊P','mkCode':161},#熊 type2=2002
	# # 认购证
	# {'types':'HKZ','code':'17149','name':'阿里瑞信一一购C','mkCode':161},#购 type2=1402
	# {'types':'HKZ','code':'15964','name':'腾讯瑞信一一购F','mkCode':161},#购 type2=1402
	# {'types':'HKZ','code':'21224','name':'腾讯中银一一购F','mkCode':161},#购 type2=1402
	# {'types':'HKZ','code':'18653','name':'阿里瑞银一一购E','mkCode':161},#购 type2=1402
	# {'types':'HKZ','code':'20120','name':'阿里摩通一一购I','mkCode':161},#购 type2=1402
	# {'types':'HKG','code':'24402','name':'港交花旗一一沽C','mkCode':161},#沽 type2=1403
	# {'types':'HKG','code':'11803','name':'港交汇丰零乙沽B','mkCode':161},#沽 type2=1403
	# {'types':'HKG','code':'15334','name':'腾讯瑞信零乙沽A','mkCode':161},#沽 type2=1403
	# {'types':'HKG','code':'14957','name':'腾讯摩通零乙沽A','mkCode':161},#沽 type2=1403
	# {'types':'HKG','code':'22409','name':'港交汇丰一一沽A','mkCode':161},#沽 type2=1403
]
codeData_US=[
	# #美股	
	{'types':'US','code':'AAPL','name':'苹果','mkCode':303},
	{'types':'US','code':'MSFT','name':'微软','mkCode':303},
	{'types':'US','code':'TSLA','name':'特斯拉','mkCode':303},
	{'types':'US','code':'NTES','name':'网易','mkCode':303},
	{'types':'US','code':'BILI','name':'哔哩哔哩','mkCode':303},
	{'types':'US','code':'MCD','name':'麦当劳','mkCode':303},
	{'types':'US','code':'BA','name':'波音','mkCode':303},
	{'types':'US','code':'DIS','name':'迪士尼','mkCode':303},
	{'types':'US','code':'BABA','name':'阿里巴巴','mkCode':303},
	{'types':'US','code':'PDD','name':'拼多多','mkCode':303},
]
codeData_activelist=list(map(lambda x:list(x.values()),codeData_active+codeData_US))
codeData_US_list=list(map(lambda x:list(x.values()),codeData_US))

codeDataUS_F10=[
	{'types':'zhishu','code':'DJI','name':'道琼斯','mkCode':303},# 没有美股指数权限
	{'types':'zhishu','code':'IXIC','name':'纳斯达克','mkCode':303},
	{'types':'zhishu','code':'SPX','name':'标普500','mkCode':303},
	{'types':'US','code':'AAPL','name':'苹果','mkCode':303},
	{'types':'US','code':'MSFT','name':'微软','mkCode':303},
	{'types':'US','code':'TSLA','name':'特斯拉','mkCode':303},
	{'types':'US','code':'NTES','name':'网易','mkCode':303},
	{'types':'US','code':'BILI','name':'哔哩哔哩','mkCode':303},
	{'types':'US','code':'MCD','name':'麦当劳','mkCode':303},
	{'types':'US','code':'BA','name':'波音','mkCode':303},
	{'types':'US','code':'DIS','name':'迪士尼','mkCode':303},
	{'types':'US','code':'BABA','name':'阿里巴巴','mkCode':303},
	{'types':'US','code':'PDD','name':'拼多多','mkCode':303},
]
codeDataUS_F10_list=list(map(lambda x:list(x.values()),codeDataUS_F10))

dataForZixuan=[
	{'codeList':['E01338','E01188','E03344','E00559','E01249','E00700','E00513','E00674','E02930','E00282','E01237','E00784','E01705','E08030','E08356','E08613','E08395','E08620','E08316','E08042','E03690','A300760','B600519']},
	{'codeList':['E01338','E01188','E03344','E00559','E01249','E00700','E00513','E00674','E02930','E00282','E01237','E00784','E01705','E08030','E08356','E08620','A300760','B600519','E08613','E08395','E03690','E08316','E08042']}
]

currExchange_Data=[
	('in','USD','HKD'),('in','HKD','USD'),('in','HKD','CNY'),('in','CNY','HKD'),('in','USD','CNY'),('in','CNY','USD'),
	('out','USD','HKD'),('out','HKD','USD'),('out','HKD','CNY'),('out','CNY','HKD'),('out','USD','CNY'),('out','CNY','USD'),
]
# currExchange_Data=[
# 	('in','USD','HKD')
# ]