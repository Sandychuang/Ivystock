# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:34:26 2018

@author: zhangshuangxi
"""
class Ivy(type):
    def __new__(cls, name, bases, atts):
        atts['author'] = ['Shuangxi Zhang']
        return type.__new__(cls, name, bases, atts)

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
    #code = ['0336.HK']
    stock = Ivystock()
   # SS.begin = SS.datetime_timestamp("2018-1-1 09:00:00")
    #stock.help()
    #stock.get(code)
    #stock.plot(code)

 #   hl50 = r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls"
   # hs300 = r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"

    #aa = stock.get_code(hs300)
    #红利50
    dd = stock.get_code('hl50')
    #stock.get_list(dd)
    stock.preprocess(dd,['Date','Close'])

    #futurelist = ['TA','RS','RM']
    #stock.get_future(futurelist)
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
        self.head=['data','close']

    def datetime_timestamp(self,dt):
        import time
    # time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return str(int(s))

    def get(self, code):
        self.code = code
        import requests
        import time
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        s = requests.Session()
        stock = str(code)
        r = s.get("https://query1.finance.yahoo.com/v7/finance/download/"+stock+"?period1="+self.begin+"&period2="+self.end+"&interval=1d&;events=history&crumb="+self.crumb,cookies=self.cookies,verify=False)
        f = open('%s.csv'% stock, 'w')
        f.write(r.text)
        f.close()
        print ('%s.csv finished' % stock)
        time.sleep(1)


    def get_list(self, codelist,marketcode=''):
        self.codelist = codelist
        self.marketcode = marketcode
        for i in range(len(self.codelist)):
            self.codeitem = '%s%s' %(self.codelist[i], self.marketcode)
            self.get(self.codeitem)


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

    def get_code(self, url, require='full'):
        self.require = require

        import pandas as pd

        codelist = {'hl50':r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls",
                    'hs300':r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"}
        try:
            self.url = codelist[url]
        except (IOError, KeyError):
            self.url = url
        code =pd.read_excel(self.url, usecols=[0, 4, 5, 7])
        code.columns = ['date', 'code','name','market']
        marketdict = {'SHH':'SS','SHZ':'SZ'}
        code['market'] = code['market'].map(lambda x :marketdict[x])
        code['code'] = code['code'].map(lambda x :str(x).zfill(6))
        codefull = []
        for i in range(len(code['code'])):
            new0 = '%s.%s'%(code['code'][i] , code['market'][i])
            codefull.append(new0)
        codeonly = list(code['code'])
        requiredict = {'full':codefull,'code':codeonly}
        result = requiredict[self.require]
        return result


    def get_future(self, futurelist):
        import urllib2
        import json
        import csv
        import time
        import os
        import datetime
        from datetime import datetime,timedelta
        self.futurelist = futurelist
        for index in xrange(len(self.futurelist)):
            html = urllib2.urlopen(r'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=%s0' % self.futurelist[index])
            hjson = json.loads(html.read())
            _OUTPUT_FILE_NAME = "%s.csv" % self.futurelist[index]
            for i in range(0,len(hjson)):
                if float(hjson[i][4])==0:
                    print ('ignore 0')
                    hjson[i][4]=hjson[i-1][4]
            with open(_OUTPUT_FILE_NAME, 'w') as out:
                csv_writer = csv.writer(out, lineterminator='\n')
                csv_writer.writerow(self.head)
                temp0=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[0][0],"%Y-%m-%d")),float(hjson[0][4]))
                csv_writer.writerow(temp0)
                for i in range(1,len(hjson)):
                    delta=int((time.mktime(time.strptime(hjson[i][0],"%Y-%m-%d"))-time.mktime(time.strptime(hjson[i-1][0],"%Y-%m-%d")))/86400)
                    if delta==1:
                        temp=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float(hjson[i][4]))
                        csv_writer.writerow(temp)
                    elif delta > 1:
                        for j in range(1,delta):
                            timeinsert=(time.mktime(time.strptime(hjson[i-1][0],"%Y-%m-%d"))+86400*(j+1))
                            timej=time.strftime("%m/%d/%Y 15:00",time.gmtime(timeinsert))
                            value=float(hjson[i][4])-float(hjson[i-1][4])
                            if value>=0:
                                temp=(timej,round((float(hjson[i-1][4])+float(j*abs(value/delta))),2))
                            else:
                                temp=(timej,round((float(hjson[i-1][4])-float(j*abs(value/delta))),2))
                                csv_writer.writerow(temp)
                        tempi=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float(hjson[i][4]))
                        csv_writer.writerow(tempi)
                    else:
                        temp=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float(hjson[i][4]))
                        csv_writer.writerow(temp)

            print ('Downloading %s finished' % self.futurelist[index])

    def preprocess(self, codelist, colume):
        self.futurelist = codelist
        self.colume = colume
        import pandas as pd
        import numpy as np
        import csv
        import time
        for index in xrange(len(self.futurelist)):
            _IUTPUT_FILE_NAME = "%s.csv" % self.futurelist[index]
            hjson = pd.read_csv(_IUTPUT_FILE_NAME)
            hjson = hjson[self.colume]
            hjson = hjson.convert_objects(convert_numeric=True)

            hjson=hjson.iloc[:,:]
            hjson=np.array(hjson)
            hjson=hjson.tolist()

            _OUTPUT_FILE_NAME = "%s.csv" % self.futurelist[index]

            with open(_OUTPUT_FILE_NAME, 'w') as out:
                csv_writer = csv.writer(out, lineterminator='\n')
                csv_writer.writerow(self.head)
                temp0=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[0][0],"%Y-%m-%d")),float('%.2f' % hjson[0][1]))
                csv_writer.writerow(temp0)
                for i in range(1,len(hjson)):
                    delta=int((time.mktime(time.strptime(hjson[i][0],"%Y-%m-%d"))-time.mktime(time.strptime(hjson[i-1][0],"%Y-%m-%d")))/86400)
                    if delta==1:
                        temp=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float('%.2f' % hjson[i][1]))
                        csv_writer.writerow(temp)
                    elif delta > 1:
                        for j in range(1,delta):
                            timeinsert=(time.mktime(time.strptime(hjson[i-1][0],"%Y-%m-%d"))+86400*(j+1))
                            timej=time.strftime("%m/%d/%Y 15:00",time.gmtime(timeinsert))
                            value=float(hjson[i][1])-float(hjson[i-1][1])
                            if value>=0:
                                temp=(timej,round((float(hjson[i-1][1])+float(j*abs(value/delta))),2))
                            else:
                                temp=(timej,round((float(hjson[i-1][1])-float(j*abs(value/delta))),2))
                            csv_writer.writerow(temp)
                        tempi=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float('%.2f' % hjson[i][1]))
                        csv_writer.writerow(tempi)
                    else:
                        temp=(time.strftime("%m/%d/%Y 15:00",time.strptime(hjson[i][0],"%Y-%m-%d")),float('%.2f' % hjson[i][1]))
                        csv_writer.writerow(temp)
            print ('Preprocessing %s finished' % self.futurelist[index])

    def get_dick(self, futurelist, phase):
        self.futurelist = futurelist

        phasedict = {'5m':'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=%s','15m':'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine15m?symbol=%s','30m':'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol=%s','60m':'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine60m?symbol=%s','1m':'http://hq.sinajs.cn/list=%s'}
        self.phase = phasedict[phase]
        import urllib2
        import json
        from pandas.core.frame import DataFrame
        html = urllib2.urlopen(self.phase % self.futurelist)
        hjson = json.loads(html.read())
        pdname = DataFrame(hjson)
        return pdname

    def get_1m(self, futurelist):
        self.futurelist = futurelist
        import urllib2
        import json
        from pandas.core.frame import DataFrame
        URL = 'http://hq.sinajs.cn/list=%s' % str(self.futurelist)
        html = urllib2.urlopen(URL)
        hjson = (html.read()).split(',')
        hjson = hjson[7:8]
        return float(hjson[0])



if __name__ == '__main__':
    #code = ['0336.HK']
    stock = Ivystock()
   # SS.begin = SS.datetime_timestamp("2018-1-1 09:00:00")
    #stock.help()
    #stock.get(code)
    #stock.plot(code)

 #   hl50 = r"http://www.csindex.com.cn/uploads/file/autofile/cons/000015cons.xls"
   # hs300 = r"http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"

    #aa = stock.get_code(hs300)
    #红利50
    #dd = stock.get_code('hl50')
    #stock.get_list(dd)
    #stock.preprocess(dd,['Date','Close'])

    #futurelist = ['TA0','RS0','RM0']
    code = 'A0'
    #stock.get_future(futurelist)
    tick = stock.get_dick(code, '5m')
    tick1m = stock.get_1m(code)


