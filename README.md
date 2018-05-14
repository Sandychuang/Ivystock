# Ivystock
[原创]做一个简洁好用的量化工具-Ivystock

    香港
    code='0336.HK'
    深市
    code='000969.SZ'
    沪市
    code='600011.SS'
    上证指数
    code='000001.SS'
    恒生指数
    code='^HSI'
    美股
    code='AAPL'
    例子
    code='600011.SS'
    SS = ivystock()
    SS.begin = SS.datetime_timestamp("2018-1-1 09:00:00")
    SS.get（code)
    SS.plot(code)

    hs300 = r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"
    aa = SS.get_code(hs300)
    #红利50
    dd = SS.get_code('hl50')
