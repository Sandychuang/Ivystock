# Ivystock
[原创]做一个简洁好用的量化工具-Ivystock

# 安装
pip install Ivystock

# 帮助
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
    
# 例子    
    
    from ivystock import ivystock as ivy

    if __name__ == '__main__':
        code = '0336.HK'
        stock = ivy.Ivystock()
        stock.begin = stock.datetime_timestamp("2018-1-1 09:00:00")
        stock.help()
        stock.get(code)
        stock.plot(code)

        hl50 = r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls"
        hs300 = r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"

        aa = stock.get_code(hs300)
        #红利50
        dd = stock.get_code('hl50')
        #stock.get_list(dd)
        #stock.preprocess(dd,['Date','Close'])

        #futurelist = ['TA0','RS0','RM0']
        #code = 'A0'
        #stock.get_future(futurelist)
        #tick = stock.get_dick(code, '5m')
        #tick1m = stock.get_1m(code)
        #futurelist=['0336.HK']
        #stock.preprocess(futurelist)
    
        
# 组团hacking

招募小伙伴，如果你有想法，有技术，可以联系我，共同hacking

![alt text](https://github-1256146603.cos.ap-shanghai.myqcloud.com/feixiong.jpg "title")
