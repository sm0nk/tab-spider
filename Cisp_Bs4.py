#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
#use sys.setdefaultencoding not solve output chaset error
#demourl=http://www.itsec.gov.cn/export/sites/itsec/person/peregester/CNITSEC2012CISE01098/
counter = 1 
for i in range(2000,2017):
    for t in ['CISE','CISA','CISO','CISM','CISE-E','CISO-E','CISM-E','CISA-E','CISP-Auditor']:
        for j in range(10000):
            SNum = "CNITSEC"+str(i)+t+"0"+str(j).zfill(4)
            url = "http://www.itsec.gov.cn/export/sites/itsec/person/peregester/%s/"% SNum
            print counter , SNum ,'  Checking .........'
            try:
                res = requests.get(url)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text,'html.parser')
                clength   = res.headers['content-length']

                if 200<= int(res.status_code) <=210 :
                    itsecid   = soup.select('.detail_title')[0].text.encode('gb2312','ignore').strip()
                    starttime = soup.select('.tdm')[0].text.encode('utf-8','ignore').strip().replace("\n","").replace("                ","")
                    endtime   = soup.select('.tdm')[1].text.encode('utf-8','ignore').strip().replace("\n","").replace("                ","")
                    username  = soup.select('.tdm')[2].text.encode('utf-8','ignore').strip()
                    authlevel = soup.select('.tdm')[3].text.encode('utf-8','ignore').strip()
                    print clength
                    print itsecid
                    print starttime
                    print endtime
                    print username
                    print authlevel
                    with open('cispall.txt','a') as f:
                        f.writelines("%s%s%s%s%s  %s\n"%(itsecid,starttime,endtime,username,authlevel,clength))
                else:
                    print SNum ,'Non-existent ########'
                counter+=1
            except:
                info=sys.exc_info()
                print 'except error'
                print info[0],":",info[1]
