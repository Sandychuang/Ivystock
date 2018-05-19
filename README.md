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
        #红利50https://github-1256146603.cos.ap-shanghai.myqcloud.com/feixiong.jpg
        dd = stock.get_code('hl50')
        
# 组团hack

招募小伙伴，如果你有想法，有技术，可以联系我，共同hacking

![alt text](https://github-1256146603.cos.ap-shanghai.myqcloud.com/feixiong.jpg "title")

# 赞助

如果这个包很合你的胃口，可以考虑赞助，赞助费用50%用于研发试验，50%将反馈给社会。

![alt text](https://github-1256146603.cos.ap-shanghai.myqcloud.com/juanzhu.jpg "title")
