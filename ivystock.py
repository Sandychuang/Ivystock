# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:34:26 2018

@author: zhangshuangxi
"""
class Ivy(type):
    pass


class Ivystock(object):
    __metaclass__ = Ivy
    def help(self):
        text = '''
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
    '''
        print(text)

    def __init__(self):
        import datetime
        self.cookies = dict(B='110nb3dddb2r2&b=3&s=i4')
        #Replace crumb=yyyy
        self.crumb = 'A857FWN.xpA'
        self.now=datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        self.begin = self.datetime_timestamp("1972-1-1 09:00:00")
        self.end = self.datetime_timestamp(self.now)

    def datetime_timestamp(self,dt):
        import time
    # time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return str(int(s))

    def get(self, code):
        self.code = code
        import requests
        s = requests.Session()
        stock = str(code)
        r = s.get("https://query1.finance.yahoo.com/v7/finance/download/"+stock+"?period1="+self.begin+"&period2="+self.end+"&interval=1d&;events=history&crumb="+self.crumb,cookies=self.cookies,verify=False)
        f = open('%s.csv'% stock, 'w')
        f.write(r.text)
        f.close()
        print ('%s.csv finished' % stock)


    def plot(self, code):
        import pandas as pd
        import matplotlib.pyplot as plt
        stock = str(code)
        es = pd.read_csv('%s.csv'% stock, index_col=0, parse_dates=False, sep=",", dayfirst=True)
        es=es.convert_objects(convert_numeric=True)
        data = pd.DataFrame({stock : es["Close"][:]})
        print(data.info())
        data.plot(subplots=True, grid=True, figsize=(8, 6))
        plt.show()

    def get_code(self, url):
        import pandas as pd

        codelist = {'hl50':r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls",
                    'hs300':r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"}
        try:
            self.url = codelist[url]
        except (IOError, KeyError):
            self.url = url
        code =pd.read_excel(self.url, usecols=[0, 4, 5])
        code.columns = ['date', 'code','name']
        code['code'] = code['code'].map(lambda x :str(x).zfill(6))
        return list(code['code'])

if __name__ == '__main__':
    code = '0336.HK'
    stock = Ivystock()
   # SS.begin = SS.datetime_timestamp("2018-1-1 09:00:00")
    stock.help()
    stock.get(code)
    stock.plot(code)

 #   hl50 = r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls"
    hs300 = r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"

    aa = stock.get_code(hs300)
    #红利50
    dd = stock.get_code('hl50')